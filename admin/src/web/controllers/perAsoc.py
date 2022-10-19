from flask import Blueprint,render_template,redirect,request,jsonify
import json,datetime,random,ast,math
from src.core.db import db_session
from src.core.models.Socio import Socio
from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json, get_all_docs_json, get_doc_json, get_all_docs_paginated_json




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

def get_all_partners_paginated_filter_json(page, value, tipo):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]
    all_pages = 1

    json = []
    result = []

    if(tipo == "nombre"):
        result = db_session.query(Socio).filter(Socio.nombre.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter(Socio.nombre.ilike("%" + value + "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
    else:
        result = db_session.query(Socio).filter(Socio.nro_socio == value).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter(Socio.nro_socio == value).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
        # TODO: Implementar el ILIKE pero con numeros
        # result = db_session.query(Socio).filter(Socio.nro_socio.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
    for row in result:
        json.append(row.json())
    return {"docs": json, "total_pages": all_pages}


@perAsoc_blueprint.route("/find/<tipo>/<value>/<page>", methods=["POST","GET"])
def buscador(page,tipo,value):
    socios_dict={"estado":tipo, "apellido":value}
    result=[] 
    if (socios_dict["apellido"] != 'vacio'):
        #if (socios_dict["estado"] == 'Activo'):
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
        return redirect ("/socios/paginado/0")

    return render_template("index_perAsoc.html", socio=result["docs"], max_page = result["total_pages"], tipo=tipo, value=value)
    
    
@perAsoc_blueprint.route("/descargarPDF/<lista>", methods=["GET"])
def descargarPDF(lista):
    lista_dict=ast.literal_eval(json.dumps(lista))
    #print(type(lista_dict))
    return render_template("prueba.html", data=lista_dict)
    
    
@perAsoc_blueprint.route("/paginado/descargarCSV/<lista>")
def descargarCSV(lista):
    return render_template("prueba.html", data=lista)
    

def get_all_partners_paginated_filter_json(page, value, tipo):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]
    all_pages = 1
    result = []

    json = []
    if(tipo == "nombre"):
        result = db_session.query(Socio).filter(Socio.nombre.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter(Socio.nombre.ilike("%" + value + "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)

        
    elif (tipo =="apellido"):
        result = db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
         
    elif (tipo == "estado"):
        result = db_session.query(Socio).filter_by(estado = value).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter_by(estado = value).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
        
    elif (tipo =="nro_socio"):
        result = db_session.query(Socio).filter(Socio.nro_socio == value).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter(Socio.nro_socio == value).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)

        # TODO: Implementar el ILIKE pero con numeros
        # result = db_session.query(Socio).filter(Socio.nro_socio.ilike("%" + value + "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
    else:
        result = db_session.query(Socio).filter_by(estado = tipo["estado"]).filter(Socio.apellido.ilike("%" + tipo["apellido"]+ "%")).limit(rows_per_page).offset(int(page)*rows_per_page)
        len_result = db_session.query(Socio).filter_by(estado = tipo["estado"]).filter(Socio.apellido.ilike("%" + tipo["apellido"]+ "%")).all()
        all_pages = math.ceil(len(len_result) / rows_per_page)
        
    for row in result:
        json.append(row.json())

    return {"docs": json, "total_pages": all_pages}

