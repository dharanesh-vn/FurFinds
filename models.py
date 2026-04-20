from sqlalchemy import Boolean, Column, Integer, String, text

from database import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    adopted = Column(Boolean, default=False, server_default=text("0"), nullable=False)
