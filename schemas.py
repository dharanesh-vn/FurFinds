from pydantic import BaseModel, ConfigDict


class PetCreate(BaseModel):
    name: str
    type: str


class PetResponse(BaseModel):
    id: int
    name: str
    type: str
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
