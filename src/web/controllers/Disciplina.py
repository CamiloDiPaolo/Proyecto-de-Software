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
    if(disc['habilitada']):
        disc['habilitada'] = True
    else:
        disc['habilitada'] = False
    create_doc_json(Disciplina,disc)
    return redirect("/admin/disciplines")

@disciplines_blueprint.route("/update/<int:id>", methods=["POST"])
def update_discipline(id):
    return jsonify(update_discipline_json(id, request.json))

@disciplines_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_discipline(id):
    return jsonify(delete_doc_json(Disciplina, id))


#@disciplines.route("/update/Status<int:id>", methods=["PUT"])
#def update_discipline_status(id):
#    return jsonify(update_discipline_status(id, request.json))

def create_discipline_json(data):
    disc = create_doc_json(Disciplina, data);
    db_session.commit()

def update_discipline_json(id, data):
    print("__________________________________")
    print(request.form)
    print(get_doc_json(Disciplina,id))
    print("__________________________________")
    #result = db_session.query(Usuario).filter_by(id = user_id).all()
    #updated_user = result[0]
    #updated_user.update(data)
    #if "roles" in data:
    #    updated_user.update_roles(data["roles"])
    #db_session.add_all([updated_user])
    #db_session.commit()
    return True#updated_user.json()

    


