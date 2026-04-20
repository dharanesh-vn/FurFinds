from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/pets", tags=["pets"])


@router.post("/", response_model=schemas.PetResponse, status_code=201)
def add_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    return crud.create_pet(db=db, pet=pet)


@router.get("/", response_model=list[schemas.PetResponse])
def list_pets(db: Session = Depends(get_db)):
    return crud.get_all_pets(db=db)


@router.post("/{id}/adopt", response_model=schemas.PetResponse)
def adopt_pet(id: int, db: Session = Depends(get_db)):
    try:
        pet = crud.adopt_pet(db=db, pet_id=id)
    except crud.PetAlreadyAdoptedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with id {id} not found.")

    return pet
