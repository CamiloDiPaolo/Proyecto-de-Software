import datetime

from sqlalchemy import Boolean, Column, Date, Float, Integer, String
from src.core.db import Base, db_session
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.core.models.Rol import Rol


class Configuracion(Base):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True)
    elementos_por_pag = Column(Integer, nullable=False)
    tabla_pagos = Column(Boolean, nullable=False)
    contacto = Column(Boolean, nullable=False)
    encabezado_pago = Column(String, nullable=False)
    valor_cuota_base = Column(Float, nullable=False)
    recargo_deuda = Column(Float, nullable=False)
    moneda = Column(String, nullable=False)


    # la configuracion no se instancia 

    def __repr__(self):
        return f"Configuracion(elementos_por_pag={self.elementos_por_pag!r}, tabla_pagos={self.tabla_pagos!r}, contacto={self.contacto!r}, encabezado_pago={self.encabezado_pago!r}, valor_cuota_base={self.valor_cuota_base!r}, recargo_deuda={self.recargo_deuda!r}, moneda={self.moneda!r})"
    
    def json(self):
        return {
            "id": self.id,
            "elementos_por_pag":  self.elementos_por_pag,
            "tabla_pagos":  self.tabla_pagos,
            "contacto":  self.contacto,
            "encabezado_pago":  self.encabezado_pago,
            "valor_cuota_base":  self.valor_cuota_base,
            "recargo_deuda":  self.recargo_deuda,
            "moneda":  self.moneda
        }
    
    def update(self, data):
        if "elementos_por_pag" in data:
            self.elementos_por_pag = data["elementos_por_pag"]
        if "tabla_pagos" in data:
            self.tabla_pagos = (data["tabla_pagos"] == 'True')
        if "contacto" in data:
            self.contacto = (data["contacto"] == 'True')
        if "encabezado_pago" in data:
            self.encabezado_pago = data["encabezado_pago"]
        if "valor_cuota_base" in data:
            self.valor_cuota_base = data["valor_cuota_base"]
        if "recargo_deuda" in data:
            self.recargo_deuda = data["recargo_deuda"]
        if "moneda" in data:
            self.moneda = data["moneda"]
