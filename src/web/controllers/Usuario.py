from flask import Blueprint, render_template, request,jsonify
from src.core.db import db_session
from src.core.models.Usuario import Usuario


users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.route("/")
def users():
    return jsonify(get_all_users_json())


def get_all_users_json():
    json = []
    result = db_session.query(Usuario).all()
    for row in result:
        json.append(row.json())
    return json