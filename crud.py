from sqlalchemy.orm import Session

import models
import schemas


class PetAlreadyAdoptedError(Exception):
    """Raised when trying to adopt a pet that is already adopted."""


def create_pet(db: Session, pet: schemas.PetCreate):
    db_pet = models.Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_all_pets(db: Session):
    return db.query(models.Pet).all()


def adopt_pet(db: Session, pet_id: int):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if pet is None:
        return None

    if pet.adopted:
        # Domain-level error; the API layer can convert this to HTTP 400/409.
        raise PetAlreadyAdoptedError(f"Pet with id {pet_id} is already adopted.")

    pet.adopted = True
    db.commit()
    db.refresh(pet)
    return pet
