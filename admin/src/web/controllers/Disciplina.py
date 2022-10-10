from flask import Blueprint, render_template, request,jsonify, redirect
from src.core.db import db_session
from src.core.models.Disciplina import Disciplina
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json

disciplines_blueprint = Blueprint("disciplines", __name__, url_prefix="/disciplines")

#@disciplines_blueprint.before_request
#def protect():
#    if(not allowed_request(request, ["admin"])):
#        return "no tenes los permisos necesarios para acceder a este request"

@disciplines_blueprint.route("/", methods=["GET"])
def all_disciplines():
    return jsonify(get_all_docs_json(Disciplina))

@disciplines_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_doc_json(Disciplina, id))

@disciplines_blueprint.route("/create", methods=["POST"])
def create_discipline():
    disc = request.form.to_dict()
    if 'habilitada' in disc.keys():
        disc['habilitada'] = True
    else:
        disc['habilitada'] = False
    create_doc_json(Disciplina,disc)
    return redirect("/admin/disciplines")

@disciplines_blueprint.route("/update/<int:id>", methods=["POST"])
def update_discipline(id):
    disc = request.form.to_dict()
    result = db_session.query(Disciplina).filter_by(id = id).all()
    if 'habilitada' in disc.keys():
        disc['habilitada'] = True
    else:
        disc['habilitada'] = False
    updated_disc = result[0]
    updated_disc.update(disc)
    db_session.add_all([updated_disc])
    db_session.commit()
    return redirect("/admin/disciplines")

@disciplines_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_discipline(id):
    return jsonify(delete_doc_json(Disciplina, id))


@disciplines_blueprint.route("/switch/<int:id>/<string:state>")
def switch(id,state):
    result = db_session.query(Disciplina).filter_by(id = id).all()
    updated_disc = result[0]
    if(state == "true"):
        updated_disc.habilitada = True;
    else:
        updated_disc.habilitada = False;
    db_session.add_all([updated_disc])
    db_session.commit()
    return redirect("/admin/disciplines")

def create_discipline_json(data):
    disc = create_doc_json(Disciplina, data);
    db_session.commit()

