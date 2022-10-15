from flask import Blueprint, render_template, request,jsonify
from src.core.db import db_session
from src.core.models.Usuario import Usuario
from src.core.models.Rol import Rol
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json, get_all_docs_paginated_json
import ast

# TODO: pulir las response, agregar codigos HTTP descriptivos
users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin"])):
        return "no tenes los permisos necesarios para acceder a este request"

@users_blueprint.route("/", methods=["GET"])
def all_users():
    return jsonify(get_all_docs_json(Usuario))

@users_blueprint.route("/page/<page>", methods=["GET"])
def all_users_paginated(page):
    return jsonify(get_all_docs_paginated_json(Usuario, page))

@users_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_doc_json(Usuario, id))

@users_blueprint.route("/create", methods=["POST"])
def create_user():
    data = request.form.to_dict()
    data["roles"] = ast.literal_eval(data["roles"] )
    return jsonify(create_user_json(data))

@users_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    return jsonify(delete_doc_json(Usuario, id))

@users_blueprint.route("/update/<id>", methods=["POST"])
def update_user(id):
    data = request.form.to_dict()
    data["roles"] = ast.literal_eval(data["roles"] )
    print(data)
    return jsonify(update_user_json(id, data))

@users_blueprint.route("/active/<id>", methods=["POST"])
def active_user(id):
    data = request.json
    return jsonify(update_user_json(id, data))

def create_user_json(data):
    new_user = create_doc_json(Usuario, data);
    new_roles = []
    for rol_id in data["roles"]:
        rol = db_session.query(Rol).filter_by(id = rol_id).all()
        new_relation = UsuarioTieneRol(new_user["id"], rol_id)
        db_session.add_all([new_relation])   
        new_roles.append(str(rol))  
    db_session.commit()
    new_user["roles"] = new_roles
    return new_user


def update_user_json(user_id, data):
    # TODO: sanitizar los parametros
    # TODO: verificar que si un dato no se pasa quede el que estaba
    print("__________________________________")
    print(data)
    print("__________________________________")
    result = db_session.query(Usuario).filter_by(id = user_id).all()
    updated_user = result[0]
    updated_user.update(data)
    if "roles" in data:
        updated_user.update_roles(data["roles"])
    db_session.add_all([updated_user])
    db_session.commit()
    return updated_user.json()
