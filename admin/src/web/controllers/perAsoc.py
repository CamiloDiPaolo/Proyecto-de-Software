from flask import Blueprint,render_template,redirect,request,jsonify
import json,datetime,random
from src.core.db import db_session
from src.core.models.Socio import Socio
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json, get_all_docs_json, get_doc_json, get_all_docs_paginated_json

import ast


perAsoc_blueprint = Blueprint('perAsoc_blueprint', __name__, url_prefix='/socios')

@perAsoc_blueprint.route("/", methods=["GET"])
def all_users():
    return redirect("/socios/paginado/0")


@perAsoc_blueprint.route("/paginado/<page>", methods=["GET"])
def socios(page):
    socios=get_all_docs_paginated_json(Socio, page)
    socios["docs"].sort(key = lambda u: u["nro_socio"])
    return render_template("index_perAsoc.html", socio=socios["docs"], max_page = socios["total_pages"])

@perAsoc_blueprint.route("/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(get_doc_json(Socio, id))

@perAsoc_blueprint.route("/crearSocio", methods=["GET"])
def createSoc():
    return render_template("create_perAsoc.html")

@perAsoc_blueprint.route("/socioCreado", methods=["POST"])
def socioCreado():
    
  
    
    #Primero sanitizar los argumentos recibidos
    result = request.form.to_dict()
    print (result)
    if (db_session.query(Socio).filter_by(nro_documento = result['nro_documento']).all()):
        return render_template("create_perAsoc.html", error='Dni ya registrado')
    
    #ASIGNO VALORES FUERA DE FORMULARIO Y AJUSTO ALGUNOS
    result['nro_socio']=random.randint(1,100000000) #verificar en base q no exista
    result['fecha_alta'] = datetime.datetime.now()
    if result['email']== '': 'null'
    if result['telefono']=='': 'null' 
    
    if result['estado']=='Activo': #in result.keys():
        result['estado'] = True
    else:
        result['estado'] = False
        
    create_doc_json(Socio, result)
    
    return redirect("/socios/")
    
@perAsoc_blueprint.route("/editarSocio/<int:id>", methods=["GET"])
def editSoc(id):
    return render_template("edit_perAsoc.html", user=get_doc_json(Socio, id))



@perAsoc_blueprint.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    disc = request.form.to_dict()
    if disc['estado']=='Activo': #in result.keys():
        disc['estado'] = True
    else:
        disc['estado'] = False
    result = db_session.query(Socio).filter_by(id = id).all()
    
    
    updated_disc = result[0]
    updated_disc.update(disc)
    db_session.add_all([updated_disc])
    db_session.commit()
    
    
    return redirect("/socios")
    

@perAsoc_blueprint.route("/delete/<int:id>", methods=["DELETE","GET"])
def deleteSoc(id):
    delete_doc_json(Socio, id)
    return redirect("/socios")


@perAsoc_blueprint.route("/find", methods=["POST","GET"])
def buscador():
    socios_dict=request.form.to_dict()
    
    print("ESTO ME LLEGO POR EL FORMULARIO ")
    print (socios_dict)
    
    socios=[]
    
    
    if (socios_dict["apellido"] != ''):
        result=db_session.query(Socio).filter_by(apellido=socios_dict["apellido"]).all()
    
    #if (socios_dict["estado"]=="activo"):
    #   result = db_session.query(Socio).filter_by(estado = True).all()
    #elif (socios_dict["estado"]=="inactivo"):
    #    result = db_session.query(Socio).filter_by(estado = False).all()
    #else:
    #    return redirect("/socios")
        
    for row in result:
        socios.append(row.json)
        
    print("ANTES DE RENDERIZAR, IMPRIMO")
    print(socios)
    return render_template("index_perAsoc.html", socio=socios)
    
    
@perAsoc_blueprint.route("/descargarPDF/<lista>", methods=["GET"])
def descargarPDF(lista):
    print("EL TIPO DE PARAMETRO ES ")
    print(type(lista))
    return render_template("prueba.html", data=lista)
    
    
@perAsoc_blueprint.route("/descargarCSV/<lista>")
def descargarCSV(lista):
    print (ast.literal_eval(lista))
    return render_template("prueba.html", data=lista)
    

def get_all_partners_paginated_filter_json(page, value, tipo):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]

    json = []
    if(tipo == "nombre"):
        result = db_session.query(Socio).filter(Socio.nombre.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
    else:
        result = db_session.query(Socio).filter(Socio.nro_socio == value).limit(rows_per_page).offset(int(page)*rows_per_page)
        # TODO: Implementar el ILIKE pero con numeros
        # result = db_session.query(Socio).filter(Socio.nro_socio.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
    for row in result:
        json.append(row.json())

    result = db_session.query(Socio).all()
    all_pages = math.floor(len(result) / rows_per_page) if math.floor(len(result) / rows_per_page) > 0 else 1
    return {"docs": json, "total_pages": all_pages}

