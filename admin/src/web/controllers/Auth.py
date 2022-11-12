import hashlib

from flask import (Blueprint, make_response, redirect, render_template,
                   request, session)
from src.core.db import db_session
from src.core.models.Usuario import Usuario

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/login", methods=["GET"])
def login_view():
    return render_template('login.html')

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.form.to_dict()
    hasher = hashlib.sha256()
    hasher.update(data["contraseña"].encode('utf-8'))
    data['contraseña'] = hasher.hexdigest()
    if not valid_user(data['username'], data['contraseña']):
        return render_template('login.html', error="alguno de los datos ingresados es incorrecto")
    
    user_id = db_session.query(Usuario.id).filter_by(username=data['username'], contraseña=data['contraseña']).all()

    session['user_id'] = user_id[0][0]

    return redirect("/admin")

@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    session.clear()

    return redirect("/admin")

def allowed_request(request, allowed_roles):
    user_id = session.get('user_id')
    if(not user_id):
        return

    user = db_session.query(Usuario).filter_by(id=user_id).all()

    if (not user):
        return
        
    user_roles = user[0].get_roles()

    for allowed_role in allowed_roles:
        for user_rol in user_roles:
            if(user_rol["nombre"] == allowed_role):
                return True
    return False
    
def valid_user(username, password):
    result = db_session.query(Usuario.username).filter_by(username=username, contraseña=password).all()
    return len(result) > 0
