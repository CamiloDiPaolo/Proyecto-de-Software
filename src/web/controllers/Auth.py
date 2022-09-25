from flask import Blueprint, render_template, request,make_response, g
from src.core.db import db_session
from src.core.models.Usuario import Usuario
import jwt


private_key = "mi-clave-privada-y-ultra-secreta-y-larga-para-firmar-jwts-podria-ser-mas-larga"


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not valid_user(request.json['username'], request.json['password']):
        return "alguno de los datos ingresados es incorrecto"
    
    user_id = db_session.query(Usuario.id).filter_by(username=request.json['username'], contraseña=request.json['password']).all()

    res = make_response("logeado")
    res.headers["Set-Cookie"] = f"jwt={sign_jwt(user_id[0][0])};path=/"

    
    return res

def allowed_request(request, allowed_roles):
    token = request.cookies.get('jwt')

    if (not token):
        return

    decoded = decode_jwt(token)
    if(not decoded):
        return

    user = db_session.query(Usuario).filter_by(id=decoded["data"]).all()
    user_roles = user[0].get_roles()

    print("---------- USER ROLES")
    print(user_roles)
    print("----------")

    for allowed_role in allowed_roles:
        for user_rol in user_roles:
            if(user_rol == allowed_role):
                return True
    return False
    
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