from flask import Blueprint,render_template,redirect,request,jsonify,flash, make_response
import json,datetime,random,ast,math
from src.core.db import db_session
from src.core.models.Socio import Socio
from src.web.controllers.Auth import allowed_request

from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json, get_all_docs_json, get_doc_json, get_all_docs_paginated_json

from src.web.controllers.PDFCreate import createPDF_perAsoc
from src.web.controllers.CSVCreate import createCSV

from src.web.validators.validatorsSocio import validate_data
import csv



perAsoc_blueprint = Blueprint('perAsoc_blueprint', __name__, url_prefix='/admin/socios')



@perAsoc_blueprint.route("/socioCreado", methods=["POST"])
def socioCreado():
    #Primero sanitizar los argumentos recibidos
    result = request.form.to_dict()
    error = validate_data(result)
    if (error):
        return render_template('create_perAsoc.html', error=error)
    
    result['nro_socio']=random.randint(1,1000000)
    print (result)
    if (db_session.query(Socio).filter_by(nro_documento = result['nro_documento']).all()) :
        return render_template("create_perAsoc.html", error='Dni ya registrado')
    
    while (db_session.query(Socio).filter_by(nro_socio = result['nro_socio']).all()):
        result['nro_socio']=random.randint(1,1000000)
        
        
    #ASIGNO VALORES FUERA DE FORMULARIO Y AJUSTO ALGUNOS
    #verificar en base q no exista
    result['fecha_alta'] = datetime.datetime.now()
    if result['email']== '': 'null'
    if result['telefono']=='': 'null' 
    
    if result['estado']=='Activo': #in result.keys():
        result['estado'] = True
    else:
        result['estado'] = False
        
    create_doc_json(Socio, result)
    
    return redirect("/admin/socios/0")
    
@perAsoc_blueprint.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    disc = request.form.to_dict()
    error = validate_data(disc,"UPDATE")
    if (error):
        return render_template('edit_perAsoc.html', error=error, user=get_doc_json(Socio, id))
    
    if disc['estado']=='Activo': #in result.keys():
        disc['estado'] = True
    else:
        disc['estado'] = False
    result = db_session.query(Socio).filter_by(id = id).all()
    
    
    updated_disc = result[0]
    updated_disc.update(disc)
    db_session.add_all([updated_disc])
    db_session.commit()
    
    
    return redirect("/admin/socios/0")
    

@perAsoc_blueprint.route("/delete/<int:id>", methods=["DELETE","GET"])
def deleteSoc(id):
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")
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
        return redirect("admin/socio/0")

    return render_template("index_perAsoc.html", socio=result["docs"], max_page = result["total_pages"], tipo=tipo, value=value, search=True)


@perAsoc_blueprint.route("/descargarPDF/<tipo>/<value>", methods=["GET"])
def descargarPDF(tipo,value):
    result=descargas(tipo, value)
    return createPDF_perAsoc(tipo,value,result)

    
    
    
@perAsoc_blueprint.route("/descargarCSV/<tipo>/<value>")
def descargarCSV(tipo,value):
    result=descargasCSV(tipo, value)
    return createCSV(result)


    

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

def descargas(tipo,value):
    socios_dict={"estado":tipo, "apellido":value}
    result=[] 
    retorno=[]
    if (socios_dict["apellido"] != 'vacio'):
        if (socios_dict["estado"]=='nada'):
            result = db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).all()
            
        elif (socios_dict["estado"]=='activo'):
            socios_dict["estado"]=True
            result=db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).filter_by(estado=True).all()
            
        elif (socios_dict["estado"]=='inactivo'):
            socios_dict["estado"]=False
            result=db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).filter_by(estado=False).all()
   
    elif (socios_dict["estado"] != 'nada'):
        
        if (socios_dict["estado"]=='activo'):
            result=db_session.query(Socio).filter_by(estado=True).all()
            
        elif (socios_dict["estado"]=='inactivo'):
            result=db_session.query(Socio).filter_by(estado=False).all()
       
            
    elif ((socios_dict["apellido"]=='vacio') & (socios_dict["estado"]=='nada')):
        result=db_session.query(Socio).all()
        
        
    for index in result:
        retorno.append(index)
    
    return retorno


def descargasCSV(tipo,value):
    socios_dict={"estado":tipo, "apellido":value}
    result=[] 
    if (socios_dict["apellido"] != 'vacio'):
        if (socios_dict["estado"]=='nada'):
            result = db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).all()
            
        elif (socios_dict["estado"]=='activo'):
            socios_dict["estado"]=True
            result=db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).filter_by(estado=True).all()
            
        elif (socios_dict["estado"]=='inactivo'):
            socios_dict["estado"]=False
            result=db_session.query(Socio).filter(Socio.apellido.ilike("%" + value + "%")).filter_by(estado=False).all()
   
    elif (socios_dict["estado"] != 'nada'):
        
        if (socios_dict["estado"]=='activo'):
            result=db_session.query(Socio).filter_by(estado=True).all()
            
        elif (socios_dict["estado"]=='inactivo'):
            result=db_session.query(Socio).filter_by(estado=False).all()
       
            
    elif ((socios_dict["apellido"]=='vacio') & (socios_dict["estado"]=='nada')):
        result=db_session.query(Socio).all()
        
    
    return result