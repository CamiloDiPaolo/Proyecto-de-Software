from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session)
from src.core.db import db_session
from src.core.models.Categoria import Categoria
from src.core.models.Configuracion import Configuracion
from src.core.models.Disciplina import Disciplina
from src.core.models.Pago import pago
from src.core.models.relations.SocioSuscriptoDisciplina import \
    SocioSuscriptoDisciplina
from src.core.models.Rol import Rol
from src.core.models.Socio import Socio
from src.core.models.Usuario import Usuario
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import (delete_doc_json, exists_entity,
                                             get_all_docs_json,
                                             get_all_docs_paginated_json,
                                             get_doc_json, update_doc_json)
from src.web.controllers.PerAsoc import get_all_partners_paginated_filter_json
from src.web.controllers.Usuario import get_all_user_paginated_filter_json

# TODO: pulir las response, agregar codigos HTTP descriptivos
admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")
@admin_blueprint.before_request
def protect():
    if(not allowed_request(request, ["admin","operador"])):
        return redirect("/auth/login")
@admin_blueprint.route("/", methods=["GET"])
def admin():
    return render_template('admin.html')
@admin_blueprint.route("/me", methods=["GET"])
def admin_me():
    user_id = session.get('user_id')
    user = db_session.query(Usuario).filter_by(id=user_id).all()
    return render_template('admin_me.html', user=user[0].json())
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
    elif(tipo == "username"):
        users = get_all_user_paginated_filter_json( page, value, "username")
    elif(tipo == "activo"):
        users = get_all_user_paginated_filter_json( page, True, "activo")
    else:
        users = get_all_user_paginated_filter_json( page, False, "activo")
    users["docs"].sort(key = lambda u: u["username"])
    return render_template('admin_usuarios.html', users=users["docs"], max_page = users["total_pages"], search = True, tipo = tipo, value = value)
@admin_blueprint.route("/users/new", methods=["GET"])
def new_user():
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")
    return render_template('admin_usuarios_new.html', roles=get_all_docs_json(Rol))
@admin_blueprint.route("/users/edit/<int:id>", methods=["GET"])
def edit_user(id):
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")
    return render_template('admin_usuarios_edit.html', user=get_doc_json(Usuario, id), roles=get_all_docs_json(Rol))

# pestaña de configuracion

@admin_blueprint.route("/config", methods=["GET"])
def config():
    config = get_doc_json(Configuracion, 1);
    return render_template('admin_configuracion.html', config=config)

@admin_blueprint.route("/config", methods=["POST"])
def update_config():
    if(not allowed_request(request, ["admin"])):
        errorMsg = "No tenes los permisos necesarios para acceder a esta función"
        flash(errorMsg)
        return redirect("/admin")
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
    if (exists_entity(Disciplina,id)):
        return render_template('admin_disciplinas_edit.html', discipline=get_doc_json(Disciplina, id), categories=get_all_docs_json(Categoria))
    else:
        errorMsg = "Error: La disciplina no existe"
        flash(errorMsg)
        return redirect('/admin/disciplines/0')

@admin_blueprint.route("/disciplines/registerMember/<int:id>", methods=["GET"])
def register_member_discipline(id):
    #Verifico que se ingrese un id valido
    if (exists_entity(Socio,id)):
        return render_template('inscribir_socio_disciplina.html', id=id, disciplines=Disciplina.get_member_available_disciplines(id), disciplinesRegistered=Disciplina.get_member_registered_disciplines(id))
    else:
        errorMsg = "Error: El socio no existe"
        flash(errorMsg)
        return redirect('/admin')

#---------------------------------------------
#Blueprints de CATEGORIAS

@admin_blueprint.route("/categories", methods=["GET"])
def categories():
    return render_template('admin_categories.html', categories=get_all_docs_json(Categoria))

@admin_blueprint.route("/categories/new", methods=["GET"])
def new_category():
    return render_template('admin_categorias_new.html', categories=get_all_docs_json(Categoria))

#---------------------------------------------
#Blueprints de PAGOS

@admin_blueprint.route("/pagos/<page>",methods=["GET"])
def payments(page):
    partners = get_all_docs_paginated_json(Socio, page)
    partners["docs"].sort(key = lambda u: u["nombre"])
    return render_template('admin_payments.html', partners=partners["docs"], max_page = partners["total_pages"])

@admin_blueprint.route("/pagos/search/<tipo>/<value>/<page>", methods=["GET"])
def partners_search_get(tipo, value, page):
    partners = []
    if(tipo == "nombre"):
        partners = get_all_partners_paginated_filter_json( page, value, "nombre")
    else:
        partners = get_all_partners_paginated_filter_json( page, value, "nro_socio")

    partners["docs"].sort(key = lambda u: u["nombre"])
    return render_template('admin_payments.html', partners=partners["docs"], max_page = partners["total_pages"], search = True, tipo = tipo, value = value)


#------------------------------------------------------
#Blueprint de SOCIOS


@admin_blueprint.route("/socios/<page>", methods=["GET"])
def socios(page):
    socios=get_all_docs_paginated_json(Socio, page)
    socios["docs"].sort(key = lambda u: u["nro_socio"])
    return render_template("index_perAsoc.html", socio=socios["docs"], max_page = socios["total_pages"])

@admin_blueprint.route("/socios/informacionSocio/<int:id>", methods=["GET"])
def infoSocio(id):
    return render_template("info_perAsoc.html", user=get_doc_json(Socio,id))

@admin_blueprint.route("/socios/crearSocio", methods=["GET"])
def createSoc():
    return render_template("create_perAsoc.html")

@admin_blueprint.route("/socios/editarSocio/<int:id>", methods=["GET"])
def editSoc(id):
    return render_template("edit_perAsoc.html", user=get_doc_json(Socio, id))

@admin_blueprint.route("/socios/delete/<int:id>", methods=["DELETE","GET"])
def deleteSoc(id):
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/socios")
    delete_doc_json(Socio, id)
    return redirect("/admin/socios/0")

@admin_blueprint.route("/socios/find/<tipo>/<value>/<page>", methods=["POST","GET"])
def buscador(page,tipo,value):
    socios_dict={"estado":tipo, "apellido":value}
    result=[] 
    if (socios_dict["apellido"] != 'vacio'):
        if (socios_dict["estado"]=='nada'):
            result=get_all_partners_paginated_filter_json(page, socios_dict["apellido"], "apellido")
        
        elif (socios_dict["estado"]=='activo'):
            socios_dict["estado"]=True
            result=get_all_partners_paginated_filter_json(page, True, socios_dict)
            
        elif (socios_dict["estado"]=='inactivo'):
            socios_dict["estado"]=False
            result=get_all_partners_paginated_filter_json(page, False, socios_dict)
        
    elif (socios_dict["estado"] != 'nada'):
        
        if (socios_dict["estado"]=='activo'):
            result=get_all_partners_paginated_filter_json(page, True, "estado")
            
        elif (socios_dict["estado"]=='inactivo'):
            result=get_all_partners_paginated_filter_json(page, False, "estado")
            
    elif ((socios_dict["apellido"]=='vacio') & (socios_dict["estado"]=='nada')):
        return redirect ("/admin/socios/0")

    return render_template("index_perAsoc.html", socio=result["docs"], max_page = result["total_pages"], tipo=tipo, value=value, search=True)
