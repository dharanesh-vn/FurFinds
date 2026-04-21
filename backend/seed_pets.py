from __future__ import annotations

from dataclasses import dataclass

from fastapi.testclient import TestClient

from main import app


@dataclass(frozen=True)
class PetTemplate:
    pet_type: str
    breed: str
    age: str
    gender: str
    vaccinated: bool
    sterilized: bool
    city: str
    shelter_name: str
    contact_person: str
    phone: str
    email: str
    description: str


TN_CITIES = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Erode",
    "Salem",
    "Trichy",
    "Karur",
    "Tiruppur",
]

DOG_BREEDS = ["Labrador", "Indie", "Beagle", "Shih Tzu", "Golden Retriever", "Pug", "Dachshund"]
CAT_BREEDS = ["Persian", "Siamese", "Maine Coon", "Indie Cat", "British Shorthair", "Ragdoll"]
BIRD_BREEDS = ["Cockatiel", "Budgie", "Lovebird", "African Grey", "Canary"]
AGES = ["Puppy", "Kitten", "Chick", "Young", "Adult", "Senior"]


def build_templates(count: int = 200) -> list[PetTemplate]:
    templates: list[PetTemplate] = []
    for idx in range(count):
        city = TN_CITIES[idx % len(TN_CITIES)]
        pet_type_selector = idx % 3
        if pet_type_selector == 0:
            pet_type = "Dog"
            breed = DOG_BREEDS[idx % len(DOG_BREEDS)]
            age = AGES[idx % len(AGES)] if AGES[idx % len(AGES)] != "Kitten" else "Young"
        elif pet_type_selector == 1:
            pet_type = "Cat"
            breed = CAT_BREEDS[idx % len(CAT_BREEDS)]
            age = AGES[idx % len(AGES)] if AGES[idx % len(AGES)] != "Puppy" else "Young"
        else:
            pet_type = "Bird"
            breed = BIRD_BREEDS[idx % len(BIRD_BREEDS)]
            age = "Young" if idx % 2 == 0 else "Adult"

        gender = "Male" if idx % 2 == 0 else "Female"
        vaccinated = idx % 4 != 0
        sterilized = idx % 5 != 0
        shelter_name = f"{city} Animal Care"
        contact_person = f"Coordinator {idx % 25 + 1}"
        phone = f"+9198765{idx:05d}"[-13:]
        email = f"shelter{idx % 40 + 1}@furfinds.org"
        description = (
            f"{breed} {pet_type.lower()} from {city}. "
            f"{'Family friendly and playful' if idx % 3 == 0 else 'Calm temperament and apartment suitable'}. "
            f"{'Low maintenance' if idx % 4 == 0 else 'Needs regular activity'}."
        )

        templates.append(
            PetTemplate(
                pet_type=pet_type,
                breed=breed,
                age=age,
                gender=gender,
                vaccinated=vaccinated,
                sterilized=sterilized,
                city=city,
                shelter_name=shelter_name,
                contact_person=contact_person,
                phone=phone,
                email=email,
                description=description,
            )
        )
    return templates


def ensure_auth(client: TestClient) -> dict[str, str]:
    email = "seed_runtime@furfinds.com"
    password = "password123"
    register_payload = {
        "name": "Seed Operator",
        "email": email,
        "phone": "9876543210",
        "city": "Chennai",
        "password": password,
    }
    client.post("/auth/register", json=register_payload)
    login = client.post("/auth/login", json={"email": email, "password": password})
    login.raise_for_status()
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def seed_pets(target_count: int = 200) -> None:
    client = TestClient(app)
    headers = ensure_auth(client)
    existing = client.get("/pets/", headers=headers)
    existing.raise_for_status()
    existing_count = len(existing.json())
    to_create = max(0, target_count - existing_count)

    templates = build_templates(target_count)
    created = 0
    for idx in range(to_create):
        template = templates[existing_count + idx]
        payload = {
            "name": f"{template.city}-{template.pet_type}-{existing_count + idx + 1}",
            "type": template.pet_type,
            "breed": template.breed,
            "age": template.age,
            "gender": template.gender,
            "vaccinated": template.vaccinated,
            "sterilized": template.sterilized,
            "description": template.description,
            "image_url": f"https://placehold.co/600x400?text={template.pet_type}+{existing_count + idx + 1}",
            "shelter_name": template.shelter_name,
            "contact_person": template.contact_person,
            "phone": template.phone,
            "email": template.email,
            "city": template.city,
        }
        response = client.post("/pets/", json=payload, headers=headers)
        response.raise_for_status()
        created += 1

    # Mark a small subset as adopted to enrich analytics and recommendation behavior.
    refreshed = client.get("/pets/", headers=headers)
    refreshed.raise_for_status()
    pets = refreshed.json()
    adopted_target = min(24, len(pets))
    adopted_count = 0
    for pet in pets:
        if adopted_count >= adopted_target:
            break
        if not pet.get("adopted"):
            adopt_response = client.post(f"/pets/{pet['id']}/adopt", headers=headers)
            if adopt_response.status_code == 200:
                adopted_count += 1

    print(f"Existing pets before seed: {existing_count}")
    print(f"Created pets: {created}")
    print(f"Total pets now: {len(pets)}")
    print(f"Adopted marked during seed: {adopted_count}")


if __name__ == "__main__":
    seed_pets(200)
