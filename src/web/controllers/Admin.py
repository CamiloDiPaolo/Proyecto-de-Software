from flask import Blueprint, render_template, request,jsonify, redirect
from src.web.controllers.Auth import allowed_request
from src.core.models.Usuario import Usuario
from src.core.models.Rol import Rol
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json

# TODO: pulir las response, agregar codigos HTTP descriptivos
admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin"])):
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        return redirect("/auth/login")

@admin_blueprint.route("/", methods=["GET"])
def admin():
    return render_template('admin.html')

@admin_blueprint.route("/users", methods=["GET"])
def users():
    return render_template('admin_usuarios.html', users=get_all_docs_json(Usuario))

@admin_blueprint.route("/users/new", methods=["GET"])
def new_user():
    return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol))

@admin_blueprint.route("/users/edit/<int:id>", methods=["GET"])
def edit_user(id):
    return render_template('admin_usuarios_edit.html', user=get_doc_json(Usuario, id), roles=get_all_docs_json(Rol))
