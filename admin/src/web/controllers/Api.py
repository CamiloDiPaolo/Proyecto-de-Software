from flask import Blueprint, jsonify, request, make_response
from src.core.db import db_session
from src.core.models.Usuario import Usuario
from src.core.models.Disciplina import Disciplina
from src.web.config import config
from src.web.controllers.FactoryCrud import get_all_docs_json, get_doc_json, update_doc_json, get_all_docs_paginated_json

import jwt

private_key = "mi-clave-privada-y-ultra-secreta-y-larga-para-firmar-jwts-podria-ser-mas-larga"

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

@api_blueprint.route("/auth", methods=["POST"])
def token():
    if not valid_user(request.json['username'], request.json['password']):
        res = make_response("alguno de los datos ingresados es incorrecto")
        res.status = 401
        return res
    
    user_id = db_session.query(Usuario.id).filter_by(username=request.json['username'], contraseña=request.json['password']).all()

    # return jsonify({"token": sign_jwt(user_id[0][0])})
    res = make_response("logeado")
    res.headers["Set-Cookie"] = f"jwt={sign_jwt(user_id[0][0])};path=/"

    return res

@api_blueprint.route("/me/profile", methods=["GET"])
def profile():
    token = request.cookies.get('jwt')

    if (not token):
        res = make_response("Tenes que loguearte para acceder a esta funcionalidad")
        res.status = 401
        return res

    decoded = decode_jwt(token)
    if(not decoded):
        res = make_response("Tenes que loguearte para acceder a esta funcionalidad")
        res.status = 401
        return res

    user = db_session.query(Usuario).filter_by(id=decoded["data"]).all()
    if (not user):
        res = make_response("Los datos de la sesion almacenada pertenecen a un usuario que ya no existe")
        res.status = 401
        return res
    
    return jsonify(user[0].json())

@api_blueprint.route("/club/disciplines", methods=["GET"])
def all_disc():
    disciplines = db_session.query(Disciplina).all()
    return jsonify(get_all_docs_json(Disciplina))


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
