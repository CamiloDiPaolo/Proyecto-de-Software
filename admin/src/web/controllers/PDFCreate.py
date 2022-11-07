from fpdf import FPDF
from flask import make_response 
from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import get_doc_json

import datetime


def transformMonth(numMonth):
    month = {"1": "Enero","2": "Febrero","3":"Marzo","4":"Abril","5":"Mayo","6":"Junio","7":"Julio","8":"Agosto","9":"Septiembre","10":"Octubre","11":"Noviembre","12":"Diciembre"}
    return month[str(numMonth)]

def createPDF_payment(partner,payment):
    config = get_doc_json(Configuracion, 1)
    encabezado = config["encabezado_pago"]
    moneda = config["moneda"]
    image_path = "https://cdve.files.wordpress.com/2017/06/cropped-cropped-logodepo1.png"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 20)
    pdf.image(name=image_path,x=10,y=10,w=30,h=30)
    pdf.text(x=45,y=20,txt=f'Recibo # {payment["id"]}')

    pdf.text(x=45,y=40,txt=f'{encabezado}')

    pdf.set_font('Arial', '', 12)
    pdf.text(x=182,y=10,txt=f'Fecha')
    pdf.text(x=180,y=15,txt=f'{datetime.datetime.now().strftime("%x")}')

    pdf.line(10,45,200,45)

    pdf.set_font('Arial', "", 16)
    pdf.text(x=30,y=55,txt=f'Recibimos de {partner["nombre"]} {partner["apellido"]}')
    pdf.text(x=30,y=60,txt=f'El importe en {moneda} ({payment["pago"]})')
    pdf.text(x=30,y=65,txt=f'Por el concepto de cuota societaria mes {transformMonth(payment["fecha"].month)} {payment["fecha"].year}')

    pdf.line(10,75,200,75)

    response = make_response(pdf.output(dest="S").encode('latin-1'))
    response.headers.set("Content-Disposition","attachment",filename="recibo.pdf")
    response.headers.set('Content-Type', 'application/pdf')
    return response

def createPDF_perAsoc(tipo,value,result):
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
