from src.core.db import Base

from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import ForeignKey


class SocioSuscriptoDisciplina(Base):
    __tablename__ = "socio_subscrito_disciplina"
    id= Column (Integer, primary_key=True)
    id_disciplina = Column(Integer,ForeignKey("disciplina.id"), nullable=False)
    id_socio = Column(Integer, ForeignKey("socio.id"), nullable=False)

    def __init__(self,id_disciplina=None, id_socio=None):
        self.id_disciplina = id_disciplina
        self.id_socio = id_socio

    def __repr__(self):
        return f"SocioSuscriptoDisciplina(id_disciplina={self.id_disciplina!r}, id_socio={self.id_socio!r})"