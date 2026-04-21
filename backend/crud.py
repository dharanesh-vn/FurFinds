from sqlalchemy.orm import Session

import models
import schemas


class PetAlreadyAdoptedError(Exception):
    """Raised when trying to adopt a pet that is already adopted."""


def create_pet(db: Session, pet: schemas.PetCreate):
    pet_data = pet.model_dump()
    pet_data["shelter_name"] = pet_data.get("shelter_name") or "FurFinds Shelter"
    pet_data["contact_person"] = pet_data.get("contact_person") or "Rescue Team"
    if pet_data.get("phone"):
        phone = str(pet_data["phone"]).replace(" ", "")
        if not phone.startswith("+91"):
            phone = f"+91{phone.lstrip('+')}"
        pet_data["phone"] = phone
    db_pet = models.Pet(**pet_data)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_all_pets(db: Session):
    return db.query(models.Pet).all()


def get_pet_by_id(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()


def update_pet(db: Session, pet_id: int, payload: schemas.PetCreate):
    pet = get_pet_by_id(db=db, pet_id=pet_id)
    if pet is None:
        return None

    pet_data = payload.model_dump()
    pet_data["shelter_name"] = pet_data.get("shelter_name") or "FurFinds Shelter"
    pet_data["contact_person"] = pet_data.get("contact_person") or "Rescue Team"
    if pet_data.get("phone"):
        phone = str(pet_data["phone"]).replace(" ", "")
        if not phone.startswith("+91"):
            phone = f"+91{phone.lstrip('+')}"
        pet_data["phone"] = phone

    for key, value in pet_data.items():
        setattr(pet, key, value)

    db.commit()
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int) -> bool:
    pet = get_pet_by_id(db=db, pet_id=pet_id)
    if pet is None:
        return False
    db.delete(pet)
    db.commit()
    return True


def get_filtered_pets(
    db: Session,
    pet_type: str | None = None,
    breed: str | None = None,
    age: str | None = None,
    gender: str | None = None,
    vaccinated: bool | None = None,
    sterilized: bool | None = None,
    city: str | None = None,
):
    query = db.query(models.Pet)
    if pet_type:
        query = query.filter(models.Pet.type.ilike(pet_type.strip()))
    if breed:
        query = query.filter(models.Pet.breed.ilike(f"%{breed.strip()}%"))
    if age:
        query = query.filter(models.Pet.age.ilike(age.strip()))
    if gender:
        query = query.filter(models.Pet.gender.ilike(gender.strip()))
    if vaccinated is not None:
        query = query.filter(models.Pet.vaccinated == vaccinated)
    if sterilized is not None:
        query = query.filter(models.Pet.sterilized == sterilized)
    if city:
        query = query.filter(models.Pet.city.ilike(city.strip()))
    return query.all()


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
