from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from math import sqrt
from typing import Iterable

import chromadb


def _normalize(vector: list[float]) -> list[float]:
    magnitude = sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return [value / magnitude for value in vector]


def _embed_text(text: str, dimensions: int = 96) -> list[float]:
    vector = [0.0] * dimensions
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for token in tokens:
        bucket = hash(token) % dimensions
        vector[bucket] += 1.0
    return _normalize(vector)


def _call_llm(preferences: str, recommendations: list[dict[str, str]]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")

    prompt = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a pet adoption assistant. Explain recommendations clearly "
                    "in 2-3 concise sentences."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"User preference: {preferences}\n"
                    f"Recommended pets: {json.dumps(recommendations)}\n"
                    "Explain why these pets fit."
                ),
            },
        ],
        "temperature": 0.4,
    }

    request = urllib.request.Request(
        api_url,
        data=json.dumps(prompt).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, TimeoutError):
        return None


class PetRecommendationService:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=".chroma")
        self.collection = self.client.get_or_create_collection(name="furfinds_pets")

    def _upsert(self, pets: Iterable[object]) -> None:
        ids: list[str] = []
        embeddings: list[list[float]] = []
        documents: list[str] = []
        metadatas: list[dict[str, str]] = []

        for pet in pets:
            profile = (
                f"{pet.name} is a {pet.age} {pet.gender} {pet.breed} {pet.type} in {pet.city}. "
                f"Health profile: vaccinated={pet.vaccinated}, sterilized={pet.sterilized}. "
                f"Description: {pet.description or 'No additional notes.'}"
            )
            ids.append(str(pet.id))
            embeddings.append(_embed_text(profile))
            documents.append(profile)
            metadatas.append(
                {
                    "name": pet.name,
                    "type": pet.type,
                    "breed": pet.breed,
                    "city": pet.city,
                }
            )

        existing = self.collection.get(include=[])
        existing_ids = existing.get("ids", [])
        if existing_ids:
            self.collection.delete(ids=existing_ids)
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )

    def recommend(self, preferences: str, pets: list[object], top_k: int) -> tuple[list[object], str]:
        available_pets = [pet for pet in pets if not pet.adopted]
        if not available_pets:
            return [], "No available pets match right now because all listed pets are adopted."

        preference_lower = preferences.lower()
        tn_cities = ["chennai", "coimbatore", "madurai", "erode", "salem"]

        preferred_city = None
        for city in tn_cities:
            if city in preference_lower:
                preferred_city = city
                break

        wants_apartment = "apartment" in preference_lower
        wants_low_maintenance = any(term in preference_lower for term in ["low maintenance", "easy care"])
        wants_family = "family" in preference_lower
        type_keywords = {"dog": "dog", "cat": "cat", "bird": "bird", "rabbit": "rabbit"}
        preferred_type = next((value for key, value in type_keywords.items() if key in preference_lower), None)

        scored: list[tuple[int, object]] = []
        for pet in available_pets:
            score = 0
            description_lower = (pet.description or "").lower()
            pet_type_lower = pet.type.lower()
            pet_breed_lower = pet.breed.lower()
            pet_city_lower = pet.city.lower()

            if preferred_city and pet_city_lower == preferred_city:
                score += 3
            if preferred_type and preferred_type == pet_type_lower:
                score += 2
            if pet.vaccinated:
                score += 1
            if pet.sterilized:
                score += 1

            if wants_apartment and (
                pet_type_lower == "cat"
                or any(word in pet_breed_lower for word in ["small", "toy", "mini", "indie"])
            ):
                score += 2

            if wants_low_maintenance and pet.vaccinated and pet.sterilized:
                score += 2

            if wants_family and any(term in description_lower for term in ["friendly", "gentle", "playful", "calm"]):
                score += 2

            for keyword in re.findall(r"[a-z0-9]+", preference_lower):
                if keyword in description_lower:
                    score += 2
                    break

            scored.append((score, pet))

        scored.sort(key=lambda item: item[0], reverse=True)
        recommendations = [pet for score, pet in scored if score > 0][: min(top_k, len(available_pets))]
        if not recommendations:
            # Keep semantic fallback to avoid empty or brittle responses.
            self._upsert(available_pets)
            query = self.collection.query(
                query_embeddings=[_embed_text(preferences)],
                n_results=min(top_k, len(available_pets)),
            )
            pet_map = {str(pet.id): pet for pet in available_pets}
            matched_ids = query.get("ids", [[]])[0]
            recommendations = [pet_map[pet_id] for pet_id in matched_ids if pet_id in pet_map]

        llm_input = [
            {
                "name": pet.name,
                "type": pet.type,
                "breed": pet.breed,
                "age": pet.age,
                "city": pet.city,
                "vaccinated": str(pet.vaccinated),
                "sterilized": str(pet.sterilized),
                "description": pet.description or "",
            }
            for pet in recommendations
        ]
        explanation = _call_llm(preferences, llm_input)
        if not explanation:
            if recommendations:
                top = recommendations[0]
                reasons: list[str] = []
                if wants_apartment and (top.type.lower() == "cat" or "small" in top.breed.lower()):
                    reasons.append("Suitable for apartment living")
                if top.vaccinated and top.sterilized:
                    reasons.append("Already vaccinated and sterilized")
                if preferred_city and top.city.lower() == preferred_city:
                    reasons.append(f"Available in {top.city}")
                if not reasons:
                    reasons.append("Good profile match based on your preferences")
                explanation = (
                    f"Recommended Pet: {top.breed} {top.type} ({top.city}). "
                    f"Reason: {'; '.join(reasons)}."
                )
            else:
                explanation = "No strong matches found for your request right now."

        return recommendations, explanation
