from sqlalchemy import Column, ForeignKey, Integer
from src.core.db import Base, db_session


class SocioSuscriptoDisciplina(Base):
    __tablename__ = "socio_subscrito_disciplina"
    id= Column (Integer, primary_key=True)
    id_disciplina = Column(Integer, nullable=False)
    id_socio = Column(Integer, nullable=False)

    def __init__(self,data):
        self.id_disciplina = data["id_disciplina"]
        self.id_socio = data["id_socio"]

    def __repr__(self):
        return f"SocioSuscriptoDisciplina(id_disciplina={self.id_disciplina!r},id_socio={self.id_socio!r})"
    
    def json(self):
        return {
            "id": self.id,
            "id_disciplina": self.id_disciplina,
            "id_socio":self.id_socio
        }
        
