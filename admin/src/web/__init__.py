from flask import Flask, request, redirect, render_template, session
from flask_session import Session

from src.web.controllers.Usuario import users_blueprint
from src.web.controllers.Auth import auth_blueprint, allowed_request
from src.web.controllers.Admin import admin_blueprint

from src.web.controllers.perAsoc import perAsoc_blueprint
from src.web.controllers.pagos import pago_blueprint
from src.web.controllers.pagos_socio import pagos_socios_blueprint
from src.web.config import config
from src.core import db
from src.web.controllers.Disciplina import disciplines_blueprint
from src.web.controllers.Categoria import categories_blueprint


def create_app(env="development", static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    db.init_app(app)
    Session(app)

    # Define home
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    # @app.route("/admin", methods=["GET"])
    # def admin():
    #     if(not allowed_request(request, ["admin"])):
    #         return redirect("/auth/login")
    #     return render_template('admin_usuarios.html')
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    app.register_blueprint(perAsoc_blueprint)
    app.register_blueprint(pago_blueprint)
    app.register_blueprint(pagos_socios_blueprint)
    app.register_blueprint(disciplines_blueprint)
    app.register_blueprint(categories_blueprint)


    return app    