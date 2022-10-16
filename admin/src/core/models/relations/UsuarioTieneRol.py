from src.core.db import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

class UsuarioTieneRol(Base):
    __tablename__ = "usuario_tiene_rol"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    rol_id = Column(Integer, nullable=False)


    def __init__(self,usuario_id=None, rol_id=None):
        self.usuario_id = usuario_id
        self.rol_id = rol_id

    def __repr__(self):
        return f"UsuarioTieneRol(usuario_id={self.usuario_id!r}, rol_id={self.rol_id!r})"