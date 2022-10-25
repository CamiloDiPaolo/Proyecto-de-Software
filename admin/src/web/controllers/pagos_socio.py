from flask import Blueprint,render_template,redirect, request,jsonify, flash
from src.core.db import db_session
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json
from src.core.models.pago import pago
from src.core.models.Socio import Socio
from src.core.models.Configuracion import Configuracion
from src.core.models.Disciplina import Disciplina
from src.core.models.relations.SocioSuscriptoDisciplina import SocioSuscriptoDisciplina
from src.web.controllers.Auth import allowed_request

from src.web.validators.validatorsPagos import validate_data

from src.web.controllers.PDFCreate import createPDF

from sqlalchemy.dialects.postgresql import Any

import datetime
import math

pagos_socios_blueprint = Blueprint("socios",__name__, url_prefix="/admin/pagos/socio")

@pagos_socios_blueprint.before_request
def protect():
   if(not allowed_request(request, ["admin","operador"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")

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
    pay = get_partner_pay(get_doc_json(Socio,id_socio))
    return render_template("create_payment.html", socio=get_doc_json(Socio,id_socio), max_date=max_date,min_date=min_date,base=pay["base"],disciplines=pay["disciplines"],rec=pay["rec"])

@pagos_socios_blueprint.route("/create",methods=["POST"])
def create_payment_POST():
    payment_dict = request.form.to_dict()
    error = validate_data(payment_dict)
    if (error):
        ac_year= datetime.datetime.now().date().year
        max_date= datetime.datetime.now().replace(year=ac_year+1,month=12,day=31).date()
        min_date= datetime.datetime.now().replace(year=ac_year-2,month=1,day=1).date()
        pay = get_partner_pay(get_doc_json(Socio,payment_dict["id_socio"]))
        return render_template("create_payment.html", socio=get_doc_json(Socio,payment_dict["id_socio"]), max_date=max_date,min_date=min_date,base=pay["base"],disciplines=pay["disciplines"],rec=pay["rec"],error=error)

    error = check_exist_payment(payment_dict["fecha"].split("-")[0],payment_dict["fecha"].split("-")[1],payment_dict["id_socio"])
    if (error):
        ac_year= datetime.datetime.now().date().year
        max_date= datetime.datetime.now().replace(year=ac_year+1,month=12,day=31).date()
        min_date= datetime.datetime.now().replace(year=ac_year-2,month=1,day=1).date()
        pay = get_partner_pay(get_doc_json(Socio,payment_dict["id_socio"]))
        return render_template("create_payment.html", socio=get_doc_json(Socio,payment_dict["id_socio"]), max_date=max_date,min_date=min_date,base=pay["base"],disciplines=pay["disciplines"],rec=pay["rec"],error=error)
    
    create_doc_json(pago,payment_dict)
    return redirect(f'/admin/pagos/socio/{payment_dict["id_socio"]}/0')

@pagos_socios_blueprint.route("/delete/<partner_id>/<id>", methods=["DELETE","GET"])
def delete_payment(partner_id,id):
    if(not allowed_request(request, ["admin"])):
        errorMsg= "No tenes el rol necesario para realizar esta acción"
        flash(errorMsg)
        return redirect("/admin/")
    delete_doc_json(pago, id)
    return redirect(f'/admin/pagos/socio/{partner_id}/0')

@pagos_socios_blueprint.route("/<partner_id>/download/<payment_id>")
def downloadPDF(partner_id,payment_id):
    partner = get_doc_json(Socio,partner_id)
    payment = get_doc_json(pago,payment_id)
    return createPDF(partner,payment)

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

    return {"docs": json, "total_pages": all_pages}

def get_partner_pay(partner):
    config = get_doc_json(Configuracion, 1)
    disciplines_ids = []
    costs = [] 
    pay= {}

    relations = db_session.query(SocioSuscriptoDisciplina).filter_by(id_socio=partner["id"]).all()
    for dis in relations:
        disciplines_ids.append(dis.id_disciplina)

    disciplines = db_session.query(Disciplina).filter(Disciplina.id.in_(disciplines_ids)).all()
    for row in disciplines:
        if(row.habilitada):
            costs.append(row.costo)

    total = sum(costs)
    pay["disciplines"] = total
    pay["base"]= config["valor_cuota_base"]
    pay["rec"] = config["recargo_deuda"]
    return pay


def check_exist_payment(year,month,id):
    rest = False
    result = db_session.query(pago).filter_by(id_socio = id).all()
    for row in result:
        rowYear = str(row.json()["fecha"]).split("-")[0]
        rowMonth = str(row.json()["fecha"]).split("-")[1]

        if(rowYear == year and rowMonth == month):
            rest = "Ya existe un pago para esa fecha"
            break
    return rest