from flask import Blueprint,render_template,redirect, request
from src.core.db import db_session
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json
from src.core.models.pago import pago
from src.core.models.socio import socio

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

import datetime

pagos_socios_blueprint = Blueprint("socios",__name__, url_prefix="/socios")

@pagos_socios_blueprint.route("/")
def socios():
    socios = get_all_docs_json(socio)
    return render_template("all_partners.html",socios=socios)

@pagos_socios_blueprint.route("/<id_socio>")
def pagos_socio(id_socio):
    pagos_socio = []
    result = db_session.query(pago).filter_by(id_socio = id_socio).all()
    for row in result:
       pagos_socio.append(row.json())
    return render_template("partner_payments.html",pagos_socio=pagos_socio,partner=get_doc_json(socio,id_socio))