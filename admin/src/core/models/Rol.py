from sqlalchemy import Boolean, Column, Date, Integer, String
from src.core.db import Base


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
    
    def json(self):
        return {
            "id":  self.id,
            "nombre":  self.nombre,
        }
