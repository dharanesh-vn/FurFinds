from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ai_recommender import PetRecommendationService
import crud
from dependencies import get_current_user
import models
from realtime import manager
import schemas
from database import get_db

router = APIRouter(prefix="/pets", tags=["pets"])
recommender = PetRecommendationService()


@router.post("/", response_model=schemas.PetResponse, status_code=201)
def add_pet(
    pet: schemas.PetCreate,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    return crud.create_pet(db=db, pet=pet)


@router.get("/", response_model=list[schemas.PetResponse])
def list_pets(
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    return crud.get_all_pets(db=db)


@router.post("/{id}/adopt", response_model=schemas.PetResponse)
async def adopt_pet(
    id: int,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    try:
        pet = crud.adopt_pet(db=db, pet_id=id)
    except crud.PetAlreadyAdoptedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with id {id} not found.")

    await manager.broadcast_json(
        {
            "event": "pet_adopted",
            "pet": {"id": pet.id, "name": pet.name, "type": pet.type, "adopted": pet.adopted},
        }
    )

    return pet


@router.post("/recommend", response_model=schemas.RecommendationResponse)
def recommend_pets(
    payload: schemas.RecommendationRequest,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    pets = crud.get_all_pets(db=db)
    recommendations, explanation = recommender.recommend(
        preferences=payload.preferences,
        pets=pets,
        top_k=payload.top_k,
    )
    return {"recommendations": recommendations, "explanation": explanation}
