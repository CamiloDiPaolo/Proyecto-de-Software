from flask import Blueprint, flash, jsonify, redirect, render_template, request
from src.core.db import db_session
from src.core.models.Categoria import Categoria
from src.web.controllers.Auth import allowed_request
from src.web.controllers.FactoryCrud import (create_doc_json, delete_doc_json,
                                             get_all_docs_json, get_doc_json)

categories_blueprint = Blueprint("categories", __name__, url_prefix="/categories")


@categories_blueprint.route("/", methods=["GET"])
def all_categories():
    return jsonify(get_all_docs_json(Categoria))


@categories_blueprint.route("/create", methods=["POST"])
def create_categories():
    cat = request.form.to_dict()
    query = db_session.query(Categoria).filter_by(nombre = cat["nombre"]).all()
    print (query)
    if (query == []):
        create_doc_json(Categoria,cat)
        successMsg = "La categoría se registro correctamente"
        flash(successMsg)
        return redirect("/admin/disciplines/0")
    else:
        errorMsg = "Error: Ya existe una categoría con ese nombre"
        flash(errorMsg)
        return redirect("/admin/categories/new")

@categories_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_categorie(id):
    return jsonify(delete_doc_json(Categoria, id))



def create_categories_json(data):
    cat = create_doc_json(Categoria, data);
    db_session.commit()
