from flask import Blueprint, render_template, request,jsonify
from src.core.db import db_session
from src.core.models.Usuario import Usuario
from src.web.controllers.Auth import allowed_request

# TODO: pulir las response, agregar codigos HTTP descriptivos
users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin"])):
        return "no tenes los permisos necesarios para acceder a este request"

@users_blueprint.route("/", methods=["GET"])
def all_users():
    return jsonify(get_all_users_json())

@users_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_user_json(id))

@users_blueprint.route("/create", methods=["POST"])
def create_user():
    return jsonify(create_user_json(request.json))

@users_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    return jsonify(delete_user_json(id))

@users_blueprint.route("/update/<int:id>", methods=["PUT"])
def update_user(id):
    return jsonify(update_user_json(id, request.json))



def get_all_users_json():
    json = []
    result = db_session.query(Usuario).all()
    for row in result:
        json.append(row.json())
    return json

def get_user_json(user_id):
    result = db_session.query(Usuario).filter_by(id = user_id).all()
    for row in result:
        return row.json()
    return {}

def create_user_json(data):
    # TODO: hashear la contraseña
    # TODO: sanitizar los parametros
    new_user = Usuario(email = data["email"], username = data["username"], contraseña = data["contraseña"], activo = False, nombre = data["nombre"], apellido = data["apellido"])
    db_session.add_all([new_user])
    db_session.commit()
    return new_user.json()

def update_user_json(user_id, data):
    # TODO: sanitizar los parametros
    # TODO: verificar que si un dato no se pasa quede el que estaba
    result = db_session.query(Usuario).filter_by(id = user_id).all()
    updated_user = result[0]
    updated_user.update(email = data["email"], username = data["username"], contraseña = data["contraseña"], activo = False, nombre = data["nombre"], apellido = data["apellido"])
    updated_user.update_roles(data["roles"])
    db_session.add_all([updated_user])
    db_session.commit()
    return updated_user.json()

def delete_user_json(user_id):
    result = db_session.query(Usuario).filter_by(id = user_id).all()
    for row in result:
        db_session.delete(row)
        db_session.commit()
    return {}