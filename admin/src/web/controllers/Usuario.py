import ast
import math

from flask import Blueprint, flash, jsonify, redirect, render_template, request
from src.core.db import db_session
from src.core.models.Configuracion import Configuracion
from src.core.models.relations.UsuarioTieneRol import UsuarioTieneRol
from src.core.models.Rol import Rol
from src.core.models.Usuario import Usuario
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import (create_doc_json, delete_doc_json,
                                             get_all_docs_json,
                                             get_all_docs_paginated_json,
                                             get_doc_json)
from src.web.validators.ValidatorsUsuario import validate_data

# TODO: pulir las response, agregar codigos HTTP descriptivos
users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")

# @users_blueprint.route("/", methods=["GET"])
# def all_users():
#     return jsonify(get_all_docs_json(Usuario))

# @users_blueprint.route("/<int:id>", methods=["GET"])
# def get_user(id):
#     return jsonify(get_doc_json(Usuario, id))
    
# @users_blueprint.route("/page/<page>", methods=["GET"])
# def all_users_paginated(page):
#     return jsonify(get_all_docs_paginated_json(Usuario, page))


@users_blueprint.route("/create", methods=["POST"])
def create_user():
    data = request.form.to_dict()

    error = validate_data(data)
    if (error):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error=error)

    error = check_exist_user(data["username"], data["email"])
    if (error):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error=error)

    if(data["roles"] == "empty"):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error="no se selecciono ningun rol")

    data["roles"] = ast.literal_eval(data["roles"] )
    create_user_json(data)
    return redirect("/admin/users/0")

@users_blueprint.route("/delete/<id>", methods=["DELETE", "GET"])
def delete_user(id):
    delete_doc_json(Usuario, id)
    return redirect("/admin/users/0")

@users_blueprint.route("/update/<id>", methods=["POST"])
def update_user(id):
    data = request.form.to_dict()

    error = validate_data(data, operation="update")
    if (error):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error=error)

    error = check_exist_user(data["username"], data["email"])
    if (error):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error=error)

    if(data["roles"] == "empty"):
        return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol), error="no se selecciono ningun rol")

    data["roles"] = ast.literal_eval(data["roles"] )
    update_user_json(id, data)
    return redirect("/admin/users/0")

@users_blueprint.route("/active/<id>", methods=["POST"])
def active_user(id):

    user = get_doc_json(Usuario, id)
    update_user_json(id, {"activo": not user["activo"]})
    return redirect("/admin/users/0")

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
    result = db_session.query(Usuario).filter_by(id = user_id).all()
    updated_user = result[0]
    updated_user.update(data)
    if "roles" in data:
        updated_user.update_roles(data["roles"])
    db_session.add_all([updated_user])
    db_session.commit()
    return updated_user.json()

def check_exist_user(username, email, id = False):
    result = db_session.query(Usuario).filter_by(username = username).all()
    for row in result:
        if (id and str(row.json()["id"]) == id):
            break
        return "ya existe un usuario con ese username"
    result = db_session.query(Usuario).filter_by(email = email).all()
    for row in result:
        if (id and str(row.json()["id"]) == id):
            break
        return "ya existe un usuario con ese email"
    return False

def get_all_user_paginated_filter_json(page, value, tipo):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]
    all_pages = 1

    json = []

    result = []
 
    if(tipo == "email"):
        result = db_session.query(Usuario).filter(Usuario.email.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Usuario).filter(Usuario.email.ilike("%" + value + "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
    elif(tipo == "username"):
        result = db_session.query(Usuario).filter(Usuario.username.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Usuario).filter(Usuario.username.ilike("%" + value + "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
    elif(tipo == "activo"):
        result = db_session.query(Usuario).filter(Usuario.activo==value).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Usuario).filter(Usuario.activo==value).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)

    for row in result:
        json.append(row.json())
    

    return {"docs": json, "total_pages": all_pages}
