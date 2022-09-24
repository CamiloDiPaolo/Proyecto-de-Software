from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

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


    def __init__(self, email=None, username=None, contraseña=None, activo=None, ultima_actualizacion=None, creacion=None, nombre=None, apellido=None):
        self.email = email
        self.username = username
        self.contraseña = contraseña
        self.activo = activo
        self.ultima_actualizacion = ultima_actualizacion
        self.creacion = creacion
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
            "apellido":  self.apellido 
        }
    
    def get_roles(self):
        return ["user", "admin"] #  cambiar esto por una relacion mas tarde