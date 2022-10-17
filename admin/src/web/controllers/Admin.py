from flask import Blueprint, render_template, request,jsonify, redirect
from src.web.controllers.Auth import allowed_request
from src.core.models.Usuario import Usuario
from src.core.models.Rol import Rol
from src.core.models.Categoria import Categoria
from src.core.models.Disciplina import Disciplina
from src.core.models.relations.SocioSuscriptoDisciplina import SocioSuscriptoDisciplina
from src.web.controllers.Usuario import get_all_user_paginated_filter_json
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

#---------------------------------------------
#Blueprints de DISCIPLINAS



@admin_blueprint.route("/disciplines/<page>", methods=["GET"])
def disciplines(page):
    disciplines = get_all_docs_paginated_json(Disciplina, page);
    disciplines["docs"].sort(key = lambda u: u["nombre"])
    return render_template('admin_disciplinas.html', disciplines=disciplines["docs"], max_page = disciplines["total_pages"])

@admin_blueprint.route("/disciplines/new", methods=["GET"])
def new_discipline():
    return render_template('admin_disciplinas_new.html', categories=get_all_docs_json(Categoria))

@admin_blueprint.route("/disciplines/edit/<int:id>", methods=["GET"])
def edit_discipline(id):
    return render_template('admin_disciplinas_edit.html', discipline=get_doc_json(Disciplina, id), categories=get_all_docs_json(Categoria))


@admin_blueprint.route("/disciplines/registerMember/<int:id>", methods=["GET"])
def register_member_discipline(id):
    return render_template('inscribir_socio_disciplina.html', id=id, disciplines=Disciplina.get_member_available_disciplines(id))


#---------------------------------------------
#Blueprints de CATEGORIAS

@admin_blueprint.route("/categories", methods=["GET"])
def categories():
    return render_template('admin_categories.html', categories=get_all_docs_json(Categoria))

@admin_blueprint.route("/categories/new", methods=["GET"])
def new_category():
    return render_template('admin_categorias_new.html', categories=get_all_docs_json(Categoria))
