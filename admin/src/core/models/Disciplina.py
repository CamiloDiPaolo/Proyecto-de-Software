from flask import jsonify
from src.core.db import Base, db_session
from src.core.models.relations.SocioSuscriptoDisciplina import SocioSuscriptoDisciplina
from src.core.models.Categoria import Categoria
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, update_doc_json, get_all_docs_paginated_json

from sqlalchemy import ForeignKey
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
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
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
        return f"Disciplina(id={self.id!r}, nombre={self.nombre!r}, categoria_id={self.categoria_id!r}, categoria_nombre={self.get_nombre_categoria()!r}, instructores={self.instructores!r}, horarios={self.horarios!r}, costo={self.costo!r}, habilitada={self.habilitada!r})"

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
    
    def get_nombre_categoria(self):
        categoria = db_session.query(Categoria.nombre).filter_by(id = self.categoria_id)
        cat= categoria[0]
        return cat.nombre

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

    def get_member_available_disciplines(id):
        disc = db_session.query(Disciplina).filter_by(habilitada=True).all()
        arraySubs= []
        arrayDisc= []
        suscriptions = db_session.query(SocioSuscriptoDisciplina).filter(SocioSuscriptoDisciplina.id_socio==id).all()
        for sub in suscriptions:
            arraySubs.append(sub.id_disciplina)
        for discipline in disc:
            if (discipline.id not in arraySubs):
                arrayDisc.append(discipline.json())
        return arrayDisc
    


    

