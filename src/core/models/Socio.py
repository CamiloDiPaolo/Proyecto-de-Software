from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date

class socio(Base):
    __tablename__ = "socio"
    id = 1#Column(Integer, primary_key=True)
    email = Column(String, primary_key=True)#Column(String, nullable=False)
    nombre = Column(String,nullable=False)
    apellido = Column(String, nullable=False)
    tipo_documento = Column(String, nullable=False)
    nro_documento = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    nro_socio = 1#Column(Integer, nullable=False)
    direccion = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False)
    telefono = Column(String, nullable=False)
    fecha_alta = '2022-09-30'#Column(Date, nullable=False)

    def __init__(self,data):
        #self.id = data["id"]
        self.email = data["email"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.tipo_documento = data["tipo_documento"]
        self.nro_documento = data["nro_documento"]
        self.genero = data["genero"]
        #self.nro_socio = data["nro_socio"]
        self.direccion = data["direccion"]
        self.estado = data["estado"]
        self.telefono = data["telefono"]
        #self.fecha_alta = data["fecha_alta"]


    def __repr__(self):
        return f"Pago(id={self.id!r}, email={self.email!r}, nombre={self.nombre!r}, apellido={self.apellido!r}, tipo_documento={self.tipo_documento!r},nro_documento={self.nro_documento!r},genero={self.genero!r},nro_socio={self.nro_socio!r},direccion={self.direccion!r},estado={self.estado!r},telefono={self.telefono!r},fecha_alta={self.fecha_alta!r},)"

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "tipo_documento": self.tipo_documento,
            "nro_documento": self.nro_documento,
            "genero": self.genero,
            "nro_socio": self.nro_socio,
            "direccion": self.direccion,
            "estado": self.estado,
            "telefono": self.telefono,
            "fecha_alta": self.fecha_alta,
        }

