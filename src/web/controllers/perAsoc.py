from flask import Blueprint,render_template,redirect,request,jsonify
import json,datetime,random

from src.core.models.Socio import socio
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json, get_all_docs_json



perAsoc_blueprint = Blueprint('perAsoc_blueprint', __name__, url_prefix='/perAsoc')

@perAsoc_blueprint.route("/", methods=["GET"])
def all_users():
    return render_template("index_perAsoc.html", socio=get_all_docs_json(socio))

@perAsoc_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_doc_json(socio, id))

@perAsoc_blueprint.route("/crearSocio", methods=["GET"])
def createSoc():
    return render_template("create_perAsoc.html")

@perAsoc_blueprint.route("/socioCreado", methods=["POST"])
def socioCreado():
    #data=sonify(request.form)
    #return redirect("/perAsoc/main")
    #print(request.form)
    result = request.form.to_dict()
    
    #ASIGNO VALORES FUERA DE FORMULARIO Y AJUSTO ALGUNOS
    result['nro_socio']=random.randint(1,100000000)
    result['fecha_alta'] = datetime.datetime.now()
    if result['email']== '': 'null'
    if result['telefono']=='': 'null' 
    if result['estado']=='Activo': #in result.keys():
        result['estado'] = True
    else:
        result['estado'] = False
    print (result['nro_socio'])
    create_doc_json(socio, result)
    return redirect("/perAsoc/")
    
@perAsoc_blueprint.route("/editarSocio", methods=["GET"])
def deleteSoc():
    return render_template("edit_perAsoc.html")


@perAsoc_blueprint.route("/delete/<id>", methods=["DELETE"])
def delete_discipline(id):
    return jsonify(delete_doc_json(socio, id))



