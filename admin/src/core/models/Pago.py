from sqlalchemy import Column, Date, Float, Integer
from src.core.db import Base


class pago(Base):
    __tablename__ = "pago"
    id = Column(Integer, primary_key=True)
    id_socio = Column(Integer, nullable=False)
    pago = Column(Float,nullable=False)
    fecha = Column(Date, nullable=False)

    def __init__(self,data):
        self.id_socio = data["id_socio"]
        self.pago = data["pago"]
        self.fecha = data["fecha"]

    def __repr__(self):
        return f"Pago(id_socio={self.id_socio!r}, pago={self.pago!r}, fecha={self.fecha!r})"

    def json(self):
        return {
            "id": self.id,
            "id_socio": self.id_socio,
            "pago": self.pago,
            "fecha": self.fecha
        }
