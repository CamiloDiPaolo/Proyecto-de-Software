from flask import Blueprint, render_template, request,jsonify, redirect, flash
from src.core.db import db_session
from src.core.models.Disciplina import Disciplina
from src.core.models.Categoria import Categoria
from src.core.models.Socio import Socio
from src.core.models.relations.SocioSuscriptoDisciplina import SocioSuscriptoDisciplina
from src.web.validators.validatorsDisciplinas import validate_data
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json, exists_entity,get_all_docs_paginated_json

disciplines_blueprint = Blueprint("disciplines", __name__, url_prefix="/disciplines")

@disciplines_blueprint.before_request
def protect():
   if(not allowed_request(request, ["admin","operador"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")

@disciplines_blueprint.route("/", methods=["GET"])
def all_disciplines():
    return jsonify(get_all_docs_json(Disciplina))

@disciplines_blueprint.route("/page/<page>", methods=["GET"])
def all_disciplines_pages(page):
    return jsonify(get_all_docs_paginated_json(Disciplina, page))

@disciplines_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_doc_json(Disciplina, id))

@disciplines_blueprint.route("/create", methods=["POST"])
def create_discipline():
    disc = request.form.to_dict()
    error = validate_data(disc)
    if (error):
        flash(error)
        return render_template('admin_disciplinas_new.html', categories=get_all_docs_json(Categoria))
    if 'habilitada' in disc.keys():
        disc['habilitada'] = True
    else:
        disc['habilitada'] = False
    create_doc_json(Disciplina,disc)
    return redirect("/admin/disciplines/0")

@disciplines_blueprint.route("/update/<int:id>", methods=["POST"])
def update_discipline(id):
    disc = request.form.to_dict()
    result = db_session.query(Disciplina).filter_by(id = id).all()
    #Chequeo que no hayan cambiado el action del form
    if(result == []):
        errorMsg = "La disciplina que queres editar no existe"
        flash(errorMsg)
        return redirect("/admin/disciplines/0")
    error = validate_data(disc,"UPDATE")
    if (error):
        flash(error)
        return render_template('admin_disciplinas_edit.html', discipline=get_doc_json(Disciplina, id), categories=get_all_docs_json(Categoria))
    if 'habilitada' in disc.keys():
        disc['habilitada'] = True
    else:
        disc['habilitada'] = False
    updated_disc = result[0]
    updated_disc.update(disc)
    db_session.add_all([updated_disc])
    db_session.commit()
    return redirect("/admin/disciplines/0")

@disciplines_blueprint.route("/delete/<id>", methods=["DELETE","GET"])
def delete_discipline(id):
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")
    #Chequeo que no hayan cambiado el id a borrar por uno invalido
    if (not exists_entity(Disciplina,id)):
        errorMsg = "Error: La disciplina a borrar no existe"
        flash(errorMsg)
    else:
        delete_doc_json(Disciplina, id)
    return redirect("/admin/disciplines/0")


@disciplines_blueprint.route("/switch/<int:id>/<string:state>")
def switch(id,state):
    result = db_session.query(Disciplina).filter_by(id = id).all()
    if (result == []):
        errorMsg = "Error: La disciplina no existe"
        flash(errorMsg)
        return redirect("/admin/disciplines/0")
    updated_disc = result[0]
    if(state == "true"):
        updated_disc.habilitada = True
    else:
        updated_disc.habilitada = False
    db_session.add_all([updated_disc])
    db_session.commit()
    return redirect("/admin/disciplines/0")

def create_discipline_json(data):
    disc = create_doc_json(Disciplina, data)
    db_session.commit()

@disciplines_blueprint.route("/addMemberDisc/<int:idDisc>/<int:idSoc>" ,methods=["GET"])
def addMemberToDiscipline(idDisc,idSoc):
    result = db_session.query(SocioSuscriptoDisciplina).filter_by(id_socio = idSoc,id_disciplina=idDisc).all()
    soc = get_doc_json(Socio,idSoc)
    #Valido que el socio exista
    if(soc == {}):
        errorMsg = "Error: El socio no existe"
        flash(errorMsg)
    #Verifico que el socio este habilitado
    elif(soc["estado"] == False):
        errorMsg = "Error: El socio no esta activo"
        flash(errorMsg)
    #Valido que el socio no este inscripto a esa disciplina
    elif(result != []):
        errorMsg = "Error: El socio ya esta inscripto a esta disciplina"
        flash(errorMsg)
    #Valido que la disciplina exista
    elif (not exists_entity(Disciplina,idDisc)):
        errorMsg = "Error: La disciplina no existe"
        flash(errorMsg)
    else:
        disc = {}
        disc["id_socio"] = idSoc
        disc["id_disciplina"] = idDisc
        membDisc = create_doc_json(SocioSuscriptoDisciplina,disc)
        successMsg = "Disciplina registrada correctamente"
        flash(successMsg)
    return redirect("/admin/disciplines/registerMember/"+str(idSoc))
