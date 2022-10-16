from flask import Blueprint, render_template, request,jsonify, redirect
from src.core.db import db_session
from src.core.models.Categoria import Categoria
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json

categories_blueprint = Blueprint("categories", __name__, url_prefix="/categories")

#@disciplines_blueprint.before_request
#def protect():
#    if(not allowed_request(request, ["admin"])):
#        return "no tenes los permisos necesarios para acceder a este request"

@categories_blueprint.route("/", methods=["GET"])
def all_categories():
    return jsonify(get_all_docs_json(Categoria))


@categories_blueprint.route("/create", methods=["POST"])
def create_categories():
    cat = request.form.to_dict()
    create_doc_json(Categoria,cat)
    return redirect("/admin/disciplines/0")

@categories_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_categorie(id):
    return jsonify(delete_doc_json(Categoria, id))


#@disciplines.route("/update/Status<int:id>", methods=["PUT"])
#def update_discipline_status(id):
#    return jsonify(update_discipline_status(id, request.json))

def create_categories_json(data):
    cat = create_doc_json(Categoria, data);
    db_session.commit()