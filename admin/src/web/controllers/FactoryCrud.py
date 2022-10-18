from flask import Blueprint, jsonify, request, make_response, session
from src.core.db import db_session
from src.core.models.Configuracion import Configuracion
import math

def get_doc_json(Model, doc_id):
    result = db_session.query(Model).filter_by(id = doc_id).all()
    for row in result:
        return row.json()
    return {}

def get_all_docs_json(Model):
    json = []
    result = db_session.query(Model).all()
    for row in result:
        json.append(row.json())
    return json


def get_all_docs_paginated_json(Model, page):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]

    json = []
    result = db_session.query(Model).limit(rows_per_page).offset(int(page)*rows_per_page)
    for row in result:
        json.append(row.json())
    
    result = db_session.query(Model).all();
    all_pages = math.ceil(len(result) / rows_per_page)
    return {"docs": json, "total_pages": all_pages}


def get_doc_json(Model, doc_id):
    result = db_session.query(Model).filter_by(id = doc_id).all()
    for row in result:
        return row.json()
    return {}


def create_doc_json(Model, data):
    # TODO: hashear la contraseña
    # TODO: sanitizar los parametros
    new_doc = Model(data)
    db_session.add_all([new_doc])
    db_session.commit()
    return new_doc.json()

def update_doc_json(Model, doc_id, data):
    # TODO: hashear la contraseña
    # TODO: sanitizar los parametros
    result = db_session.query(Model).filter_by(id = doc_id).all()
    updated_doc = result[0]
    updated_doc.update(data)
    db_session.commit()
    return updated_doc.json()

def delete_doc_json(Model, doc_id):
    result = db_session.query(Model).filter_by(id = doc_id).all()
    for row in result:
        db_session.delete(row)
        db_session.commit()

    return {}

def check_role(role):
    id= session["user_id"]
    arrayRoles = []
    roles= get_all_docs_json(Rol)
    for row in roles:
        arrayRoles.append(row)
    usuarioTieneRoles= get_all_docs_json(usuarioTieneRoles)
    print(arrayRoles)
    return usuarioTieneRoles

#Para verificar si existe un determinado elemento
def exists_entity(Model,id):
    entity = get_doc_json(Model,id)
    if (entity == {}):
        return False
    return True

