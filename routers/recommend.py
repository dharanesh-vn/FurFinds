from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_recommender import PetRecommendationService
import crud
from dependencies import get_current_user
import models
import schemas
from database import get_db

router = APIRouter(tags=["recommend"])
recommender = PetRecommendationService()


@router.post("/recommend", response_model=schemas.RecommendationResponse)
def recommend(
    payload: schemas.RootRecommendationRequest,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    pets = crud.get_all_pets(db=db)
    recommendations, explanation = recommender.recommend(
        preferences=payload.preference_text,
        pets=pets,
        top_k=payload.top_k,
    )
    return {"recommendations": recommendations, "explanation": explanation}
