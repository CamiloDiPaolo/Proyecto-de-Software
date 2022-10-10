from flask import Blueprint,render_template,redirect, request
from src.core.db import db_session
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json
from src.core.models.pago import pago
from src.core.models.Socio import Socio

import datetime

pagos_socios_blueprint = Blueprint("socios",__name__, url_prefix="/socios")

@pagos_socios_blueprint.route("/")
def socios():
    socios = get_all_docs_json(Socio)
    return render_template("all_partners.html",socios=socios)

@pagos_socios_blueprint.route("/<id_socio>")
def pagos_socio(id_socio):
    pagos_socio = []
    result = db_session.query(pago).filter_by(id_socio = id_socio).order_by(pago.fecha.desc()).all()
    for row in result:
       pagos_socio.append(row.json())
    return render_template("partner_payments.html",pagos_socio=pagos_socio,partner=get_doc_json(socio,id_socio),ac_year=datetime.datetime.now().year)

@pagos_socios_blueprint.route("/find",methods=["GET"])
def find_partenr():
    partner_dict = request.args.to_dict()
    partenrs = []
    #  and type(partner_dict["search"]) is str
    if(partner_dict["type"] == "nombre"):
        result = db_session.query(socio).filter_by(nombre = partner_dict["search"]).all()
    elif(partner_dict["type"] == "nro_socio"):
        result = db_session.query(socio).filter_by(nro_socio = partner_dict["search"]).all()
    else:
       return redirect("/socios") 
    for row in result:
       partenrs.append(row.json())
    return render_template("all_partners.html",socios=partenrs)

