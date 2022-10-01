from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre= Column(String, nullable=False)

    def __init__(self,data):
        self.nombre = data["nombre"]

    def __repr__(self):
        return f"Categoria(id={self.id!r}, nombre={self.nombre!r})"

    def json(self):
        return {
            "id":  self.id,
            "nombre":  self.nombre,
        }
    def getName():
        return self.nombre
        
    