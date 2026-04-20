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
    by_type: dict[str, int] = {}
    by_city: dict[str, int] = {}
    by_age: dict[str, int] = {}
    vaccinated_count = 0
    not_vaccinated_count = 0

    for pet in pets:
        by_type[pet.type] = by_type.get(pet.type, 0) + 1
        by_city[pet.city] = by_city.get(pet.city, 0) + 1
        by_age[pet.age] = by_age.get(pet.age, 0) + 1
        if pet.vaccinated:
            vaccinated_count += 1
        else:
            not_vaccinated_count += 1

    return {
        "total_pets": total_pets,
        "adopted_count": adopted_count,
        "adoption_rate": round(adoption_rate, 4),
        "by_type": by_type,
        "by_city": by_city,
        "vaccination": {"vaccinated": vaccinated_count, "not_vaccinated": not_vaccinated_count},
        "by_age": by_age,
    }
