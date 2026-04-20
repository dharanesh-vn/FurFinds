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
            profile = f"{pet.name} is a {pet.type} pet and is available for adoption."
            ids.append(str(pet.id))
            embeddings.append(_embed_text(profile))
            documents.append(profile)
            metadatas.append({"name": pet.name, "type": pet.type})

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

        self._upsert(available_pets)
        query = self.collection.query(
            query_embeddings=[_embed_text(preferences)],
            n_results=min(top_k, len(available_pets)),
        )

        pet_map = {str(pet.id): pet for pet in available_pets}
        matched_ids = query.get("ids", [[]])[0]
        recommendations = [pet_map[pet_id] for pet_id in matched_ids if pet_id in pet_map]

        llm_input = [{"name": pet.name, "type": pet.type} for pet in recommendations]
        explanation = _call_llm(preferences, llm_input)
        if not explanation:
            names = ", ".join(pet.name for pet in recommendations)
            explanation = (
                f"For '{preferences}', these pets are the closest semantic match: {names}. "
                "They align with your request based on pet type and availability."
            )

        return recommendations, explanation
