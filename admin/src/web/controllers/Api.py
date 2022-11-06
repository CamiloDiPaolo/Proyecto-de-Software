from flask import Blueprint, jsonify, request, make_response, session, Response
from src.core.db import db_session
from src.core.models.Usuario import Usuario
from src.core.models.Disciplina import Disciplina
from src.core.models.pago import pago
from src.core.models.relations.SocioSuscriptoDisciplina import SocioSuscriptoDisciplina
from src.web.config import config
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, update_doc_json, get_all_docs_paginated_json
import hashlib

import jwt

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
    res.headers["Set-Cookie"] = f"jwt={sign_jwt(user_id[0][0])};path=/;SameSite=None;Secure"
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

@api_blueprint.route("/club/disciplines", methods=["GET"])
def all_disc():
    disciplines = db_session.query(Disciplina).all()
    return jsonify(get_all_docs_json(Disciplina))

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
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)

    # por ahora se hardcodea
    res = jsonify([{"name": "fulvo", "cant": 20}, {"name": "waterpolo", "cant": 10}, {"name": "polo", "cant": 50}])
    return cors(res)

## Endpoints de PAGOS
@api_blueprint.route("/me/payments", methods=["GET"])
def my_payments():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)
    
    return jsonify(payments[0].json())

@api_blueprint.route("/me/payments", methods=["POST"])
def my_paymentsPost():
    token = request.cookies.get('jwt')
    error = error_logged(token)
    if(error):
        res = jsonify({"status": 401, "message": error})
        return cors(res)

    payment_dict = request.form.to_dict()
    return jsonify(create_doc_json(pago,payment_dict))

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

    # por ahora se hardcodea; total => total de usuarios; morosos => usuarios morosos
    res = jsonify({"total": 100, "morosos": 25})
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

    # por ahora se hardcodea
    res = jsonify({"active": 10, "inactive": 20})
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
    # token = request.cookies.get('jwt')
    if (not token): 
        return "No estas logeado"

    decoded = decode_jwt(token)
    if(not decoded):
        return "el token no es valido"

    user = db_session.query(Usuario).filter_by(id=decoded["data"]).all()
    if (not user):
        return "la sesion pertenece a un usuario que no existe"
    return False


def cors(res):
    # res.headers.add("Access-Control-Allow-Origin", "http://localhost:5173)
    # res.headers.add("Access-Control-Allow-Origin", "https://grupo21.proyecto2022.linti.unlp.edu.ar")
    res.headers.add("Access-Control-Allow-Headers", "X-Requested-With,content-type")
    res.headers.add("Access-Control-Allow-Methods", "*")
    res.headers.add("Access-Control-Allow-Credentials", "true")
    return res
