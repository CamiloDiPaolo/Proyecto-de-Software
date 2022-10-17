from flask import Blueprint,render_template,redirect, request,send_file
from src.core.db import db_session
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json
from src.core.models.pago import pago
from src.core.models.Socio import Socio
from src.core.models.Configuracion import Configuracion
from src.web.controllers.PDFCreate import createPDF

import datetime
import math

pagos_socios_blueprint = Blueprint("socios",__name__, url_prefix="/admin/pagos/socio")

@pagos_socios_blueprint.route("/")
def socios():
   return redirect("/admin/pagos/0")

@pagos_socios_blueprint.route("/<id_socio>/<page>")
def pagos_socio(id_socio,page):
    partner_payments = get_all_partners_payments_paginated_filter_json( page, id_socio)
    partner_payments["docs"].sort(key = lambda u: u["fecha"])
    return render_template("partner_payments.html",partner_payments=partner_payments["docs"],partner=get_doc_json(Socio,id_socio),max_page=partner_payments["total_pages"],ac_year=datetime.datetime.now().year)

@pagos_socios_blueprint.route("/<id_socio>/new")
def create_payment(id_socio):
    ac_year= datetime.datetime.now().date().year
    max_date= datetime.datetime.now().replace(year=ac_year+1,month=12,day=31).date()
    min_date= datetime.datetime.now().replace(year=ac_year-2,month=1,day=1).date()
    return render_template("create_payment.html", socio=get_doc_json(Socio,id_socio), max_date=max_date,min_date=min_date)

@pagos_socios_blueprint.route("/create",methods=["POST"])
def create_payment_POST():
    payment_dict = request.form.to_dict()
    create_doc_json(pago,payment_dict)
    return redirect(f'/admin/pagos/socio/{payment_dict["id_socio"]}')

@pagos_socios_blueprint.route("/delete/<partner_id>/<id>", methods=["DELETE","GET"])
def delete_payment(partner_id,id):
    delete_doc_json(pago, id)
    return redirect(f'/admin/pagos/socio/{partner_id}/0')

@pagos_socios_blueprint.route("/<partner_id>/download/<payment_id>")
def downloadPDF(partner_id,payment_id):
    partner = get_doc_json(Socio,partner_id)
    payment = get_doc_json(pago,payment_id);
    print("--------------------------")
    print(partner)
    print("--------------------------")
    print(payment)
    print("--------------------------")

    return send_file(createPDF(partner,payment),download_name="recibo.pdf",mimetype='image/pdf',as_attachment=True)

def get_all_partners_payments_paginated_filter_json(page, value):
    config = get_doc_json(Configuracion, 1)
    rows_per_page = config["elementos_por_pag"]
    all_pages = 1

    json = []
    result = []

    result = db_session.query(pago).filter(pago.id_socio == value).limit(rows_per_page).offset(int(page)*rows_per_page)
    len_result = db_session.query(pago).filter(pago.id_socio == value).all()
    all_pages = math.ceil(len(len_result) / rows_per_page)

    for row in result:
        json.append(row.json())

    print("--------------------------")
    print(json)
    print("--------------------------")
    return {"docs": json, "total_pages": all_pages}