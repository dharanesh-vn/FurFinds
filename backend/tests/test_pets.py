from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db
from main import app
import models
from security import hash_password


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pets.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def auth_headers(client: TestClient, email: str = "user@mail.com", password: str = "password123") -> dict:
    register_payload = {
        "name": "User",
        "email": email,
        "phone": "9876543210",
        "city": "Chennai",
        "password": password,
    }
    client.post("/auth/register", json=register_payload)
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def sample_pet_payload(
    name: str,
    pet_type: str,
    breed: str = "Mixed Breed",
    city: str = "Chennai",
) -> dict:
    return {
        "name": name,
        "type": pet_type,
        "breed": breed,
        "age": "Adult",
        "gender": "Male",
        "vaccinated": True,
        "sterilized": True,
        "description": f"{name} is friendly and playful.",
        "image_url": "https://placehold.co/200x120",
        "shelter_name": "FurFinds Shelter",
        "contact_person": "Rescue Team",
        "phone": "+919876543210",
        "email": "shelter@furfinds.com",
        "city": city,
    }


def test_register_and_login(client: TestClient) -> None:
    register_response = client.post(
        "/auth/register",
        json={
            "name": "User",
            "email": "user@mail.com",
            "phone": "9876543210",
            "city": "Chennai",
            "password": "password123",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json()["role"] == "user"

    duplicate_response = client.post(
        "/auth/register",
        json={
            "name": "User",
            "email": "user@mail.com",
            "phone": "9876543210",
            "city": "Chennai",
            "password": "password123",
        },
    )
    assert duplicate_response.status_code == 400

    login_response = client.post(
        "/auth/login",
        json={"email": "user@mail.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_create_pet(client: TestClient) -> None:
    headers = auth_headers(client)
    response = client.post(
        "/pets/",
        json=sample_pet_payload(name="Bruno", pet_type="Dog", breed="Labrador Mix"),
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Bruno"
    assert body["type"] == "Dog"
    assert body["breed"] == "Labrador Mix"
    assert body["city"] == "Chennai"
    assert body["adopted"] is False


def test_get_pets(client: TestClient) -> None:
    headers = auth_headers(client)
    client.post("/pets/", json=sample_pet_payload(name="Bruno", pet_type="Dog"), headers=headers)
    client.post("/pets/", json=sample_pet_payload(name="Luna", pet_type="Cat"), headers=headers)

    response = client.get("/pets/", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["name"] == "Bruno"
    assert body[1]["name"] == "Luna"


def test_get_pet_by_id(client: TestClient) -> None:
    headers = auth_headers(client)
    created = client.post("/pets/", json=sample_pet_payload(name="Bella", pet_type="Dog"), headers=headers).json()

    response = client.get(f"/pets/{created['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Bella"


def test_get_pet_by_invalid_id_returns_404(client: TestClient) -> None:
    headers = auth_headers(client)
    response = client.get("/pets/999", headers=headers)
    assert response.status_code == 404


def test_update_pet(client: TestClient) -> None:
    headers = auth_headers(client)
    created = client.post("/pets/", json=sample_pet_payload(name="Flash", pet_type="Cat"), headers=headers).json()
    payload = sample_pet_payload(name="Flash Updated", pet_type="Cat", breed="Siamese", city="Madurai")

    response = client.put(f"/pets/{created['id']}", json=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Flash Updated"
    assert body["breed"] == "Siamese"
    assert body["city"] == "Madurai"


def test_delete_pet(client: TestClient) -> None:
    headers = auth_headers(client)
    created = client.post("/pets/", json=sample_pet_payload(name="Ruby", pet_type="Rabbit"), headers=headers).json()

    delete_response = client.delete(f"/pets/{created['id']}", headers=headers)
    assert delete_response.status_code == 200

    fetch_response = client.get(f"/pets/{created['id']}", headers=headers)
    assert fetch_response.status_code == 404


def test_delete_pet_invalid_id_returns_404(client: TestClient) -> None:
    headers = auth_headers(client)
    response = client.delete("/pets/999", headers=headers)
    assert response.status_code == 404


def test_get_pets_with_filters(client: TestClient) -> None:
    headers = auth_headers(client)
    client.post(
        "/pets/",
        json=sample_pet_payload(name="Coco", pet_type="Cat", breed="Persian", city="Coimbatore"),
        headers=headers,
    )
    client.post(
        "/pets/",
        json=sample_pet_payload(name="Max", pet_type="Dog", breed="Indie Mix", city="Chennai"),
        headers=headers,
    )

    response = client.get("/pets/?type=Cat&city=Coimbatore&vaccinated=true", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Coco"
    assert body[0]["city"] == "Coimbatore"


def test_adopt_pet_successfully(client: TestClient) -> None:
    headers = auth_headers(client)
    create_response = client.post("/pets/", json=sample_pet_payload(name="Bruno", pet_type="Dog"), headers=headers)
    pet_id = create_response.json()["id"]

    response = client.post(f"/pets/{pet_id}/adopt", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == pet_id
    assert body["adopted"] is True


def test_prevent_adopting_already_adopted_pet(client: TestClient) -> None:
    headers = auth_headers(client)
    create_response = client.post("/pets/", json=sample_pet_payload(name="Bruno", pet_type="Dog"), headers=headers)
    pet_id = create_response.json()["id"]
    client.post(f"/pets/{pet_id}/adopt", headers=headers)

    response = client.post(f"/pets/{pet_id}/adopt", headers=headers)

    assert response.status_code == 400
    assert "already adopted" in response.json()["detail"].lower()


def test_adopt_nonexistent_pet_returns_404(client: TestClient) -> None:
    headers = auth_headers(client)
    response = client.post("/pets/999/adopt", headers=headers)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_recommend_pets_returns_matches_and_explanation(client: TestClient) -> None:
    headers = auth_headers(client)
    client.post(
        "/pets/",
        json=sample_pet_payload(name="Nibbles", pet_type="Rabbit", breed="Mini Lop"),
        headers=headers,
    )
    client.post(
        "/pets/",
        json=sample_pet_payload(name="Rocky", pet_type="Dog", breed="Indie Mix"),
        headers=headers,
    )

    response = client.post(
        "/pets/recommend",
        json={"preferences": "small pet for apartment", "top_k": 1},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) == 1
    assert body["recommendations"][0]["adopted"] is False
    assert body["explanation"]


def test_root_recommend_endpoint_returns_matches_and_explanation(client: TestClient) -> None:
    headers = auth_headers(client)
    client.post("/pets/", json=sample_pet_payload(name="Peanut", pet_type="Rabbit"), headers=headers)
    client.post("/pets/", json=sample_pet_payload(name="Bolt", pet_type="Dog"), headers=headers)

    response = client.post(
        "/recommend",
        json={"preference_text": "small pet for apartment", "top_k": 2},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["recommendations"]) >= 1
    assert "explanation" in body
    assert body["explanation"]


def test_analytics_endpoint_returns_totals_and_rate(client: TestClient) -> None:
    headers = auth_headers(client)
    client.post("/pets/", json=sample_pet_payload(name="Bruno", pet_type="Dog"), headers=headers)
    luna = client.post("/pets/", json=sample_pet_payload(name="Luna", pet_type="Cat"), headers=headers).json()
    client.post(f"/pets/{luna['id']}/adopt", headers=headers)

    response = client.get("/analytics", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total_pets"] == 2
    assert body["adopted_count"] == 1
    assert body["adoption_rate"] == 0.5
    assert "Dog" in body["by_type"]
    assert "Cat" in body["by_type"]
    assert "Chennai" in body["by_city"]
    assert "vaccinated" in body["vaccination"]


def test_admin_users_requires_admin_role(client: TestClient) -> None:
    user_headers = auth_headers(client, email="member@mail.com")
    forbidden = client.get("/admin/users", headers=user_headers)
    assert forbidden.status_code == 403


def test_admin_users_allowed_for_admin_role(client: TestClient) -> None:
    db = TestingSessionLocal()
    admin = models.User(
        name="Admin Dharanesh",
        email="admin@furfinds.com",
        phone=None,
        city=None,
        hashed_password=hash_password("Admin@123"),
        role="admin",
    )
    db.add(admin)
    db.commit()
    db.close()

    login_response = client.post(
        "/auth/login",
        json={"email": "admin@furfinds.com", "password": "Admin@123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
