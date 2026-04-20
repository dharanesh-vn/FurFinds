from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db
from main import app


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


def test_create_pet(client: TestClient) -> None:
    response = client.post("/pets/", json={"name": "Bruno", "type": "Dog"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Bruno"
    assert body["type"] == "Dog"
    assert body["adopted"] is False


def test_get_pets(client: TestClient) -> None:
    client.post("/pets/", json={"name": "Bruno", "type": "Dog"})
    client.post("/pets/", json={"name": "Luna", "type": "Cat"})

    response = client.get("/pets/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["name"] == "Bruno"
    assert body[1]["name"] == "Luna"


def test_adopt_pet_successfully(client: TestClient) -> None:
    create_response = client.post("/pets/", json={"name": "Bruno", "type": "Dog"})
    pet_id = create_response.json()["id"]

    response = client.post(f"/pets/{pet_id}/adopt")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == pet_id
    assert body["adopted"] is True


def test_prevent_adopting_already_adopted_pet(client: TestClient) -> None:
    create_response = client.post("/pets/", json={"name": "Bruno", "type": "Dog"})
    pet_id = create_response.json()["id"]
    client.post(f"/pets/{pet_id}/adopt")

    response = client.post(f"/pets/{pet_id}/adopt")

    assert response.status_code == 400
    assert "already adopted" in response.json()["detail"].lower()


def test_adopt_nonexistent_pet_returns_404(client: TestClient) -> None:
    response = client.post("/pets/999/adopt")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
