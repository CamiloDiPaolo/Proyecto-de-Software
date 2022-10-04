from flask import Blueprint,render_template,redirect, request
from src.core.db import db_session
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, create_doc_json, delete_doc_json
from src.core.models.pago import pago
from src.core.models.socio import socio

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

import datetime

pago_blueprint = Blueprint("pagos",__name__, url_prefix="/pagos")



@pago_blueprint.route("/")
def redirection():
    return redirect("/socios")

@pago_blueprint.route("/<id_socio>/new")
def create_payment(id_socio):
        return render_template("create_payment.html", socio=get_doc_json(socio,id_socio), ac_year=datetime.datetime.now().date().year)

@pago_blueprint.route("create",methods=["POST"])
def create_payment_POST():
    payment_dict = request.form.to_dict()
    print("----------------------")
    print(payment_dict)
    print("----------------------")
    data = {
        "id_socio": payment_dict["id_socio"],
        "pago": payment_dict["Pago"],
        "fecha": datetime.date(int(payment_dict["Año"]),int(payment_dict["month"]),1)
    }
    print(data)
    create_doc_json(pago,data)
    return redirect("/socios/"+ data["id_socio"])