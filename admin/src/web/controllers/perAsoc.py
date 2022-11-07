from flask import Blueprint,render_template,redirect,request,jsonify,flash, make_response
import json,datetime,random,ast,math
from src.core.db import db_session
from src.core.models.Socio import Socio
from src.web.controllers.Auth import allowed_request

from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import create_doc_json, delete_doc_json, get_all_docs_json, get_doc_json, get_all_docs_paginated_json
from fpdf import FPDF
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
    print(result)
    pdf=FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    image_path = "https://cdve.files.wordpress.com/2017/06/cropped-cropped-logodepo1.png"
    pdf.image(name=image_path,x=10,y=8,w=30,h=30)
    
    
    if (value != 'vacio'): #apellido cargado
        
        if (tipo=='nada'): #estado sin cargar
            pdf.text(x=50,y=25,txt=f'Tabla De Socios filtrada por apellido: {value}')
        
        else: #estado cargado
            pdf.text(x=82,y=21,txt=f'Tabla De Socios filtrada por:')
            pdf.text(x=74, y=28, txt=f'Apellido: {value} y Estado: {tipo}')
              
    else: #apellido sin cargar
        if (tipo=='nada'): #Estado sin cargar
            pdf.text(x=60,y=25,txt=f'Tabla De Socios sin filtrar ')    
        else: #Estado cargado
            pdf.text(x=60,y=25,txt=f'Tabla De Socios filtada por Estado: {tipo}')
    pdf.line(0, 45, 256, 45) 
    pdf.ln(40) 

    #CREO LA TABLA
    pdf.set_fill_color(r= 184, g=190 , b=250)
    pdf.cell(w=50,h=15, txt='Nro socio', border = 1, align='C', fill=1)
    pdf.cell(w=50,h=15, txt='Nombre', border = 1, align='C', fill=1)
    pdf.cell(w=50,h=15, txt='Apellido', border = 1, align='C', fill=1)
    pdf.cell(w=40,h=15, txt='Estado', border = 1, align='C', ln=1, fill=1)
    
    pdf.set_fill_color(r=232 , g=232 , b=232)

    print(type(result))

    for socio in result:
        pdf.cell(w=50,h=15, txt=str(socio.nro_socio), border = 1, align='C', fill=1)
        pdf.cell(w=50,h=15, txt=socio.nombre, border = 1, align='C', fill=1)
        pdf.cell(w=50,h=15, txt=socio.apellido, border = 1, align='C', fill=1)
        if (socio.estado == True):
            pdf.cell(w=40,h=15, txt='Activo', border = 1, align='C', ln=1, fill=1)
        else:
            pdf.cell(w=40,h=15, txt='Inactivo', border = 1, align='C', ln=1, fill=1)
     
    response = make_response(pdf.output(dest="S").encode('latin-1'))
    response.headers.set("Content-Disposition","attachment",filename="tabla_de_socios.pdf")
    response.headers.set('Content-Type', 'application/pdf')
    return response
    
    
@perAsoc_blueprint.route("/descargarCSV/<tipo>/<value>")
def descargarCSV(tipo,value):
    result=descargas(tipo, value) 
    with open('listado.csv', 'w', newline='')as csvfile:
        fieldnames=['nro_socio','email','nombre','apellido','tipo_documento','nro_documento']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        
        for socio in result:
            thewriter.writerow({'nro_socio':socio['nro_socio'],'email':socio['email'],'nombre':socio['nombre'],'apellzido':socio['apellido'],'tipo_documento':socio['tipo_documento'],'nro_documento':socio['nro_documento']})
            
    response = make_response(csvfile)
    response.headers.set("Content-Disposition","attachment",filename="listado.csv")
    response.headers.set('Content-Type', 'application/csv')
    return response


    

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