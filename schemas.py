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
