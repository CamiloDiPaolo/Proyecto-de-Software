from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)


    def __init__(self,nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return f"Rol(nombre={self.nombre!r})"
    
    def __str__(self):
        return self.nombre