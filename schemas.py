from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PetCreate(BaseModel):
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    breed: str = Field(min_length=1)
    age: str = "Adult"
    gender: Literal["Male", "Female"] = "Female"
    vaccinated: bool = False
    sterilized: bool = False
    description: str | None = None
    image_url: str | None = None
    shelter_name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    city: str = Field(min_length=1)


class PetResponse(BaseModel):
    id: int
    name: str
    type: str
    breed: str
    age: str
    gender: str
    vaccinated: bool
    sterilized: bool
    description: str | None
    image_url: str | None
    shelter_name: str
    contact_person: str
    phone: str | None
    email: str | None
    city: str
    adopted: bool

    model_config = ConfigDict(from_attributes=True)


class RecommendationRequest(BaseModel):
    preferences: str
    top_k: int = 3


class RootRecommendationRequest(BaseModel):
    preference_text: str
    top_k: int = 3


class RecommendationResponse(BaseModel):
    recommendations: list[PetResponse]
    explanation: str


class AnalyticsResponse(BaseModel):
    total_pets: int
    adopted_count: int
    adoption_rate: float
    by_type: dict[str, int]
    by_city: dict[str, int]
    vaccination: dict[str, int]
    by_age: dict[str, int]


class UserRegister(BaseModel):
    name: str
    email: str
    phone: str | None = None
    city: str | None = None
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    city: str | None
    role: str

    model_config = ConfigDict(from_attributes=True)
