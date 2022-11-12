import datetime
import hashlib

from sqlalchemy import Boolean, Column, Date, Integer, String
from src.core.db import Base, db_session
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.core.models.Rol import Rol


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


    def __init__(self, data):
        self.ultima_actualizacion = datetime.datetime.now()
        self.creacion = datetime.datetime.now()

        self.email = data["email"]
        self.username = data["username"]

        # hasheamos las contraseñas
        hasher = hashlib.sha256()
        hasher.update(data["contraseña"].encode('utf-8'))
        self.contraseña = hasher.hexdigest()


        if "activo" in data:
            self.activo = data["activo"]
        else:
            self.activo = True
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]

    def __repr__(self):
        return f"Usuario(email={self.email!r}, username={self.username!r}, contraseña={self.contraseña!r}, activo={self.activo!r}, ultima_actualizacion={self.ultima_actualizacion!r}, creacion={self.creacion!r}, nombre={self.nombre!r}, apellido={self.apellido!r})"


    def json(self):
        return {
            "id": self.id,
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
            roles.append(rol[0].json())
        return roles 
    
    def update(self, data):
        if "email" in data:
            self.email = data["email"]
        if "username" in data:
            self.username = data["username"]
        if "contraseña" in data:
            hasher = hashlib.sha256()
            hasher.update(data["contraseña"].encode('utf-8'))
            self.contraseña = hasher.hexdigest()
        if "activo" in data:
            self.activo = data["activo"]
        self.ultima_actualizacion = datetime.datetime.now()
        if "nombre" in data:
            self.nombre = data["nombre"]
        if "apellido" in data:
            self.apellido = data["apellido"]
    
    def update_roles(self, roles):
        # TODO: refactorizar esto...
        if(len(roles) == 0):
            return
        # eliminamos las antiguas relaciones
        old_roles = db_session.query(UsuarioTieneRol).filter_by(usuario_id = self.id).all()
        for old_relation in old_roles:
            db_session.delete(old_relation)
        
        # creamos las nuevas relaciones
        for role in roles:
            new_relation = UsuarioTieneRol(self.id, role)
            db_session.add_all([new_relation])
        
        db_session.commit()


