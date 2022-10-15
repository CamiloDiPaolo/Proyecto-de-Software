from src.core.db import Base, db_session
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.core.models.Categoria import Categoria

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import Float

import datetime

class Disciplina(Base):
    __tablename__ = "disciplina"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    categoria_id = Column(Integer, nullable=False)
    instructores = Column(String, nullable=False)
    horarios = Column(String, nullable=False)
    costo = Column(Float, nullable=False)
    habilitada = Column(Boolean, nullable=False)

    def __init__(self, data):
        self.nombre = data["nombre"]
        self.categoria_id = data["categoria_id"]
        self.instructores = data["instructores"]
        self.horarios = data["horarios"]
        self.costo = data["costo"]
        self.habilitada = data["habilitada"]

    def __repr__(self):
        return f"Disciplina(id={self.id!r}, nombre={self.nombre!r}, categoria_id={self.categoria_id!r}, instructores={self.instructores!r}, horarios={self.horarios!r}, costo={self.costo!r}, habilitada={self.habilitada!r})"

    def json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.get_categoria(),
            "instructores": self.instructores,
            "horarios": self.horarios,
            "costo": self.costo,
            "habilitada": self.habilitada 
        }
    
    def get_categoria(self):
        categoria = db_session.query(Categoria).filter_by(id = self.categoria_id)
        cat= categoria[0].json()
        return cat
    
    def update(self, data):
        if "nombre" in data:
            self.nombre = data["nombre"]
        if "instructores" in data:
            self.instructores = data["instructores"]
        if "horarios" in data:
            self.horarios = data["horarios"]
        if "costo" in data:
            self.costo = data["costo"]
        if "habilitada" in data:
            self.habilitada = data["habilitada"]
        if "categoria_id" in data:
            self.categoria_id = data["categoria_id"]

