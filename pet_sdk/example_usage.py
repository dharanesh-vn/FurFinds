"""
Example usage for the generated FurFinds Python SDK.

Run from project root:
    python pet_sdk/example_usage.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make generated package importable without installing it.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import openapi_client
from openapi_client.models.pet_create import PetCreate
from openapi_client.rest import ApiException


def main() -> None:
    configuration = openapi_client.Configuration(host="http://127.0.0.1:8000")

    with openapi_client.ApiClient(configuration) as api_client:
        pets_api = openapi_client.PetsApi(api_client)

        # Fetch pets
        pets = pets_api.list_pets_pets_get()
        print(f"Found {len(pets)} pet(s).")
        for pet in pets:
            print(f"- #{pet.id}: {pet.name} ({pet.type}) adopted={pet.adopted}")

        # If no pets exist, create one so adopt flow can be demonstrated
        if not pets:
            created = pets_api.add_pet_pets_post(PetCreate(name="Bruno", type="Dog"))
            print(f"Created pet #{created.id}: {created.name}")
            pets = [created]

        # Adopt the first available pet
        candidate = next((pet for pet in pets if not pet.adopted), None)
        if candidate is None:
            print("No available pets to adopt.")
            return

        adopted = pets_api.adopt_pet_pets_id_adopt_post(candidate.id)
        print(f"Adopted pet #{adopted.id}: {adopted.name} (adopted={adopted.adopted})")


if __name__ == "__main__":
    try:
        main()
    except ApiException as exc:
        print(f"API call failed: {exc}")
