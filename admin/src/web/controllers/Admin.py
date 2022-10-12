from flask import Blueprint, render_template, request,jsonify, redirect
from src.web.controllers.Auth import allowed_request
from src.core.models.Usuario import Usuario
from src.web.controllers.Usuario import get_all_user_paginated_filter_json
from src.core.models.Rol import Rol
from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, update_doc_json, get_all_docs_paginated_json
from src.core.models.Socio import Socio
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json

# TODO: pulir las response, agregar codigos HTTP descriptivos
admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin"])):
        return redirect("/auth/login")

@admin_blueprint.route("/", methods=["GET"])
def admin():
    return render_template('admin.html')

# pestaña de usuarios

@admin_blueprint.route("/users/<page>", methods=["GET"])
def users(page):
    users = get_all_docs_paginated_json(Usuario, page);
    users["docs"].sort(key = lambda u: u["username"])
    return render_template('admin_usuarios.html', users=users["docs"], max_page = users["total_pages"])

# @admin_blueprint.route("/users/search/<page>", methods=["POST"])
# def users_search(page):
#     users = []
#     data = request.form.to_dict()
#     if(data["type_search"] == "email"):
#         users = get_all_user_paginated_filter_json( page, data["input_search"], "email")
#     else:
#         users = get_all_user_paginated_filter_json( page, data["input_search"], "username")

#     users["docs"].sort(key = lambda u: u["username"])
#     return render_template('admin_usuarios.html', users=users["docs"], max_page = users["total_pages"], search = True)

@admin_blueprint.route("/users/search/<tipo>/<value>/<page>", methods=["GET"])
def users_search_get(tipo, value, page):
    users = []
    if(tipo == "email"):
        users = get_all_user_paginated_filter_json( page, value, "email")
    else:
        users = get_all_user_paginated_filter_json( page, value, "username")

    users["docs"].sort(key = lambda u: u["username"])
    return render_template('admin_usuarios.html', users=users["docs"], max_page = users["total_pages"], search = True, tipo = tipo, value = value)

@admin_blueprint.route("/users/new", methods=["GET"])
def new_user():
    return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol))

@admin_blueprint.route("/users/edit/<int:id>", methods=["GET"])
def edit_user(id):
    return render_template('admin_usuarios_edit.html', user=get_doc_json(Usuario, id), roles=get_all_docs_json(Rol))

# pestaña de configuracion

@admin_blueprint.route("/config", methods=["GET"])
def config():
    config = get_doc_json(Configuracion, 1);
    return render_template('admin_configuracion.html', config=config)

@admin_blueprint.route("/config", methods=["POST"])
def update_config():
    data = request.form.to_dict()
    update_doc_json(Configuracion, 1, data)
    return redirect("/admin/config")

#RUTAS DE SOCIOS

@admin_blueprint.route("perAsoc", methods=["GET"])
def disciplines():
    return render_template('index_perAsoc.html', socio=get_all_docs_json(Socio))

@admin_blueprint.route("/perAsoc/crearSocio", methods=["GET"])
def new_discipline():
    return render_template('create_perAsoc.html', categories=get_all_docs_json(Socio))

@admin_blueprint.route("/perAsoc/editarSocio/<int:id>", methods=["GET"])
def edit_discipline(id):
    return render_template('edit_perAsoc.html', discipline=get_doc_json(Socio, id), categories=get_all_docs_json(Socio))

