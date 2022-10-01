from flask import Blueprint,render_template,redirect,request,jsonify
import json

from src.core.models.Socio import socio
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json



perAsoc_blueprint = Blueprint('perAsoc_blueprint', __name__, url_prefix='/perAsoc')

@perAsoc_blueprint.route("/main", methods=["GET"])
def main ():
    return render_template("index_perAsoc.html")

@perAsoc_blueprint.route("/crearSocio", methods=["GET"])
def createSoc():
    return render_template("create_perAsoc.html")

@perAsoc_blueprint.route("/socioCreado", methods=["POST"])
def socioCreado():
    #data=sonify(request.form)
    #return redirect("/perAsoc/main")
    #print(request.form)
    result = request.form.to_dict(flat=False)
    print(result)
    #result.id=1
    #result.nro_socio=1
    json_objeto=create_doc_json(socio, result)
    return render_template("pruebanashe.html",data=result)
    
@perAsoc_blueprint.route("/editarSocio", methods=["GET"])
def deleteSoc():
    return render_template("edit_perAsoc.html")


