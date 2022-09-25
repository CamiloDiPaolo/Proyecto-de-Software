from src.core.db import Base, db_session
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.core.models.Rol import Rol

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

import datetime

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    contraseña = Column(String, nullable=False)
    activo = Column(Boolean, nullable=False)
    ultima_actualizacion = Column(Date, nullable=False)
    creacion = Column(Date, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)


    def __init__(self, email=None, username=None, contraseña=None, activo=None, nombre=None, apellido=None):
        self.email = email
        self.username = username
        self.contraseña = contraseña
        self.activo = activo
        self.ultima_actualizacion = datetime.datetime.now()
        self.creacion = datetime.datetime.now()
        self.nombre = nombre
        self.apellido = apellido

    def __repr__(self):
        return f"Usuario(email={self.email!r}, username={self.username!r}, contraseña={self.contraseña!r}, activo={self.activo!r}, ultima_actualizacion={self.ultima_actualizacion!r}, creacion={self.creacion!r}, nombre={self.nombre!r}, apellido={self.apellido!r})"

    # def __str__(self):
    #     return f"Hola, mi nombre es ${self.username}"

    def json(self):
        return {
            "email":  self.email,
            "username":  self.username,
            "contraseña":  self.contraseña,
            "activo":  self.activo,
            "ultima_actualizacion":  self.ultima_actualizacion,
            "creacion":  self.creacion,
            "nombre":  self.nombre,
            "apellido":  self.apellido,
            "roles": self.get_roles() 
        }
    
    def get_roles(self):
        roles = []
        result = db_session.query(UsuarioTieneRol).filter_by(usuario_id = self.id).all()
        for row in result:
            rol = db_session.query(Rol).filter_by(id = row.rol_id).all()
            roles.append(rol[0].__str__())
        return roles 
    
    def update(self, email=None, username=None, contraseña=None, activo=None, nombre=None, apellido=None):
        self.email = email
        self.username = username
        self.contraseña = contraseña
        self.activo = activo
        self.ultima_actualizacion = datetime.datetime.now()
        self.nombre = nombre
        self.apellido = apellido

