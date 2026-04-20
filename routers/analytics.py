from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from dependencies import get_current_user
import models
import schemas
from database import get_db

router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_model=schemas.AnalyticsResponse)
def get_analytics(
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    pets = crud.get_all_pets(db=db)
    total_pets = len(pets)
    adopted_count = sum(1 for pet in pets if pet.adopted)
    adoption_rate = (adopted_count / total_pets) if total_pets else 0.0
    return {
        "total_pets": total_pets,
        "adopted_count": adopted_count,
        "adoption_rate": round(adoption_rate, 4),
    }
