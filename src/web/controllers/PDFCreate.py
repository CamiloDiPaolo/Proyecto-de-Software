from fpdf import FPDF

import datetime


def transformMonth(numMonth):
    month = {"1": "Enero","2": "Febrero","3":"Marzo","4":"Abril","5":"Mayo","6":"Junio","7":"Julio","8":"Agosto","9":"Septiembre","10":"Octubre","11":"Noviembre","12":"Diciembre"}
    return month[str(numMonth)]


def createPDF(partner,payment):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 20)
    pdf.image("src\web\static\img\logo_club.png",x=10,y=10,w=30,h=30,type="png")
    pdf.text(x=45,y=20,txt=f'Recibo # {payment["id"]}')

    pdf.set_font('Arial', '', 12)
    pdf.text(x=182,y=10,txt=f'Fecha')
    pdf.text(x=180,y=15,txt=f'{datetime.datetime.now().strftime("%x")}')

    pdf.line(10,45,200,45)

    pdf.set_font('Arial', "", 16)
    pdf.text(x=30,y=55,txt=f'Recibimos de {partner["nombre"]} {partner["apellido"]}')
    pdf.text(x=30,y=60,txt=f'El importe en pesos ({payment["pago"]})')
    pdf.text(x=30,y=65,txt=f'Por el concepto de cuota societaria mes {transformMonth(payment["fecha"].month)} {payment["fecha"].year}')

    pdf.line(10,75,200,75)

    return pdf.output("tuto1.pdf","F")