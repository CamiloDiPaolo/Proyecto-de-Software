from fpdf import FPDF
from flask import make_response 
from src.core.models.Configuracion import Configuracion
from src.web.controllers.FactoryCrud import get_doc_json

import datetime


def transformMonth(numMonth):
    month = {"1": "Enero","2": "Febrero","3":"Marzo","4":"Abril","5":"Mayo","6":"Junio","7":"Julio","8":"Agosto","9":"Septiembre","10":"Octubre","11":"Noviembre","12":"Diciembre"}
    return month[str(numMonth)]

def createPDF(partner,payment):
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