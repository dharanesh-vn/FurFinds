from sqlalchemy import Boolean, Column, Integer, String, Text, text

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default=text("'user'"))


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    breed = Column(String, index=True, nullable=False, server_default=text("'Mixed Breed'"))
    age = Column(String, nullable=False, server_default=text("'Adult'"))
    gender = Column(String, nullable=False, server_default=text("'Female'"))
    vaccinated = Column(Boolean, nullable=False, server_default=text("0"))
    sterilized = Column(Boolean, nullable=False, server_default=text("0"))
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    shelter_name = Column(String, nullable=False, server_default=text("'FurFinds Shelter'"))
    contact_person = Column(String, nullable=False, server_default=text("'Rescue Team'"))
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    city = Column(String, index=True, nullable=False, server_default=text("'Chennai'"))
    adopted = Column(Boolean, default=False, server_default=text("0"), nullable=False)
