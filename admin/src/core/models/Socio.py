import hashlib

from sqlalchemy import Boolean, Column, Date, Integer, String
from src.core.db import Base


class Socio(Base):
    __tablename__ = "socio"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False) 
    nombre = Column(String,nullable=False)
    apellido = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tipo_documento = Column(String, nullable=False)
    nro_documento = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    nro_socio = Column(Integer, nullable=False)
    direccion = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False)
    telefono = Column(String, nullable=False)
    fecha_alta = Column(Date, nullable=False)

    def __init__(self,data):
        self.email = data["email"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.tipo_documento = data["tipo_documento"]
        self.nro_documento = data["nro_documento"]
        self.genero = data["genero"]
        self.nro_socio = data["nro_socio"]
        self.direccion = data["direccion"]
        self.estado = data["estado"]
        self.telefono = data["telefono"]
        self.fecha_alta = data["fecha_alta"]
        
        #Hasheo la contraseña para guardar en la BD
        hasher = hashlib.sha256()
        hasher.update(data["pass"].encode('utf-8'))
        self.password = hasher.hexdigest()



    def __repr__(self):
        return f"id={self.id!r}, email={self.email!r}, nombre={self.nombre!r}, apellido={self.apellido!r}, pass={self.password!r}, tipo_documento={self.tipo_documento!r},nro_documento={self.nro_documento!r},genero={self.genero!r},nro_socio={self.nro_socio!r},direccion={self.direccion!r},estado={self.estado!r},telefono={self.telefono!r},fecha_alta={self.fecha_alta!r},)"

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "password": self.password,
            "tipo_documento": self.tipo_documento,
            "nro_documento": self.nro_documento,
            "genero": self.genero,
            "nro_socio": self.nro_socio,
            "direccion": self.direccion,
            "estado": self.estado,
            "telefono": self.telefono,
            "fecha_alta": self.fecha_alta,
        }
        
    def update(self, data):
        if "email" in data:
            self.email = data["email"]
        if "nombre" in data:
            self.nombre = data["nombre"]
        if "apellido" in data:
            self.apellido = data["apellido"]
        if "estado" in data:
            self.estado = data["estado"]
        if "genero" in data:
            self.genero = data["genero"]
        if "direccion" in data:
            self.direccion = data["direccion"]
        if "telefono" in data:
            self.telefono = data["telefono"]
            
