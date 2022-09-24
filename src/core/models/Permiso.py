from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

class Permiso(Base):
    __tablename__ = "permiso"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)


    def __init__(self,nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return f"Permiso(nombre={self.nombre!r})"