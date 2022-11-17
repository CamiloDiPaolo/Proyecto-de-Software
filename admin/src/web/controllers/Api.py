import hashlib
import datetime
import jwt
from flask import Blueprint, jsonify, make_response, request, session
from src.core.db import db_session
from src.core.models.Disciplina import Disciplina
from src.core.models.Pago import pago
from src.core.models.Socio import Socio
from src.core.models.relations.SocioSuscriptoDisciplina import \
    SocioSuscriptoDisciplina
from src.core.models.Usuario import Usuario
from src.web.config import config
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, update_doc_json, get_all_docs_paginated_json, create_doc_json
from sqlalchemy import func

import hashlib

import jwt
import datetime

private_key = "mi-clave-privada-y-ultra-secreta-y-larga-para-firmar-jwts-podria-ser-mas-larga"

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

# Metemos esto pq flask nose pq toma una peticion de OPTIONS ¿¿¿¿¿¿??????
@api_blueprint.route("/auth", methods=[ "OPTIONS"])
def token_2():
    return cors(make_response())

@api_blueprint.route("/auth", methods=["POST"])
def token():
    print(request.json)
    hasher = hashlib.sha256()
    hasher.update(request.json['password'].encode('utf-8'))
    request.json['password'] = hasher.hexdigest()
    print(request.json)
    if not valid_user(request.json['username'], request.json['password']):
        res = jsonify({"status": 401, "message": "Los datos ingresados no son correctos"})
        return cors(res)
    
    user_id = db_session.query(Usuario.id).filter_by(username=request.json['username'], contraseña=request.json['password']).all()

    res = jsonify({"status": 200})
    res.headers["Set-Cookie"] = f"jwt={sign_jwt(user_id[0][0])};path=/;SameSite=None;Secure" #USO REMOTO
    #res.headers["Set-Cookie"] = f"jwt={sign_jwt(user_id[0][0])};path=/;" #USO LOCAL
    print(res.headers)
    return cors(res)

# Metemos esto pq flask nose pq toma una peticion de OPTIONS ¿¿¿¿¿¿??????
@api_blueprint.route("/me/profile", methods=[ "OPTIONS"])
def profile_2():
    return cors(make_response())

@api_blueprint.route("/me/profile", methods=["GET"])
def profile():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)

    decoded = decode_jwt(token)
    user = db_session.query(Usuario).filter_by(id=decoded["data"]).all()
    res = make_response(user[0].json())
    return cors(res)

## Endpoints de DISCIPLINAS    

@api_blueprint.route("/club/disciplines", methods=["OPTIONS"])
def all_disc_2():
    return cors(make_response())

@api_blueprint.route("/club/disciplines", methods=["GET"])
def all_disc():
    disciplines = db_session.query(Disciplina).all()
    res = jsonify(get_all_docs_json(Disciplina))
    return cors(res)


@api_blueprint.route("/club/info", methods=["OPTIONS"])
def get_club_info2():
    return cors(make_response())

@api_blueprint.route("club/info", methods=["GET"])
def get_club_info():
    res = {
        "email": "clubdeportivovillaelisa@gmail.com",
        "phone": "0221 487-0193"
    }
    res = jsonify(res)
    return cors(res)


@api_blueprint.route("/discipline/<id>", methods=[ "OPTIONS"])
def  get_disc2(id):
    return cors(make_response())

@api_blueprint.route("/discipline/<id>", methods=["GET"])
def get_disc(id):
    res = jsonify(get_doc_json(Disciplina,id))
    return cors(res)



@api_blueprint.route("/me/disciplines", methods=["GET"])
def my_disciplines():    
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)

    disciplines = get_user_disciplines(decoded["data"])
    return jsonify(disciplines)

@api_blueprint.route("/disciplines/cant", methods=[ "OPTIONS"])
def disciplines_cant_2():
    return cors(make_response())

@api_blueprint.route("/disciplines/cant", methods=["GET"])
def disciplines_cant():
    disciplines = db_session.query(Disciplina).all()
    cantidades = []
    for discipline in disciplines:
            cantidad = db_session.query(SocioSuscriptoDisciplina).filter_by(id_disciplina = discipline.id).count()
            count = {"name": discipline.nombre, "cant": cantidad}
            cantidades.append(count)
    res = jsonify(cantidades)
    return cors(res)

## Endpoints de PAGOS
@api_blueprint.route("/me/payments", methods=[ "OPTIONS"])
def  my_payments2():
    return cors(make_response())

@api_blueprint.route("/me/payments", methods=["GET"])
def my_payments():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)
    json = []
    decoded = decode_jwt(token)
    ac_year= datetime.datetime.now().date().year
    user_payments = db_session.query(pago).filter(pago.id_socio == decoded["data"]).order_by(pago.fecha).all()
    for payment in user_payments:
        if(payment.fecha.year == ac_year):
            json.append(payment.json())

    res = make_response(json)
    return cors(res)

@api_blueprint.route("/me/payments", methods=["POST"])
def my_paymentsPost():
    res = {}
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})

    payment = request.json
    print("-----------------------------")
    print(payment)
    print("-----------------------------")

    if(not validateType(payment["certificate"])):
        res = jsonify({
            "status": 400, "message": "El tipo no es vlaido"
        })
    decoded = decode_jwt(token)
    user_id = decoded["data"]
    if(paymentExist(payment,user_id)):
        res = jsonify({
            "status": 400, "message": "El mes ingresado ya esta pago"
        })

    newPayment = {
        "id_socio": user_id,
        "pago": payment["pay"],
        "fecha": payment["date"]
    }
    if(not res):
        if(create_doc_json(pago,newPayment)) :
            res = jsonify({"status": 200, "message": "El pago se subio correctamente"})
        else: 
            res = jsonify({"status": 400, "message": "Ocurrio un error al subir el pago"})

    return cors(res)
    


@api_blueprint.route("/socios/morosos", methods=[ "OPTIONS"])
def socios_morosos_2():
    return cors(make_response())

@api_blueprint.route("/socios/morosos", methods=["GET"])
def socios_morosos():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)

    days = { 1: 31, 2:28, 3:31, 4:30, 5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    ac_year= datetime.datetime.now().date().year
    ac_month = datetime.datetime.now().date().month
    firstDate = datetime.datetime(ac_year,ac_month,1)
    lastDate = datetime.datetime(ac_year,ac_month,days[ac_month])

    allUsers = db_session.query(Socio).count()
    defaulters = db_session.query(pago).join(Socio, Socio.id == pago.id_socio).filter(pago.fecha.between(firstDate,lastDate)).count()

    res = jsonify({"total": allUsers, "morosos": allUsers - defaulters})
    return cors(res)

## Endpoints de socios
@api_blueprint.route("/socios/actives", methods=[ "OPTIONS"])
def socios_activos_2():
    return cors(make_response())

@api_blueprint.route("/socios/actives", methods=["GET"])
def socios_activos():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)
    cantidadActivos = db_session.query(Socio).filter_by(estado = True).count()
    cantidadInactivos = db_session.query(Socio).filter_by(estado = False).count()
    res = jsonify({"active": cantidadActivos, "inactive": cantidadInactivos})
    return cors(res)

    

# Funciones Auxiliares

def get_user_disciplines(id):
        disc = db_session.query(Disciplina).all()
        arraySubs= []
        arrayDisc= []
        suscriptions = db_session.query(SocioSuscriptoDisciplina).filter(SocioSuscriptoDisciplina.id_socio==id).all()
        for sub in suscriptions:
            arraySubs.append(sub.id_disciplina)
        for discipline in disc:
            if (discipline.id in arraySubs):
                arrayDisc.append(discipline.json())
        return arrayDisc

def valid_user(username, password):
    result = db_session.query(Usuario.username).filter_by(username=username, contraseña=password).all()
    return len(result) > 0

def sign_jwt(data):
    return jwt.encode({"data": data}, private_key)

def decode_jwt(jwt_signed):
    try:
        decoded_jwt = jwt.decode(jwt_signed, options={"verify_signature": False})
        return decoded_jwt
    except:
        return False

def error_logged(token):
    #token = request.cookies.get('jwt')
    if (not token): 
        return "No estas logeado"

    decoded = decode_jwt(token)
    if(not decoded):
        return "el token no es valido"

    user = db_session.query(Usuario).filter_by(id=decoded["data"]).all()
    if (not user):
        return "la sesion pertenece a un usuario que no existe"
    return False

def validateType(certificate):
    return certificate.endswith((".jpg",".png",".pdf"))

def paymentExist(payment,id):
    year = str(payment["date"]).split("-")[0]
    month = str(payment["date"]).split("-")[1]
    rest = False
    result = db_session.query(pago).filter_by(id_socio = id).all()
    for row in result:
        rowYear = str(row.json()["fecha"]).split("-")[0]
        rowMonth = str(row.json()["fecha"]).split("-")[1]

        if(rowYear == year and rowMonth == month):
            rest = True
            break
    return rest

def cors(res):
    #res.headers.add("Access-Control-Allow-Origin", "http://localhost:5173") #USO LOCAL
    res.headers.add("Access-Control-Allow-Origin", "https://grupo21.proyecto2022.linti.unlp.edu.ar") #USO REMOTO
    res.headers.add("Access-Control-Allow-Headers", "X-Requested-With,content-type")
    res.headers.add("Access-Control-Allow-Methods", "*")
    res.headers.add("Access-Control-Allow-Credentials", "true")
    return res
