from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from src.core import db
from src.web.config import config
from src.web.controllers.Admin import admin_blueprint
from src.web.controllers.Api import api_blueprint
from src.web.controllers.Auth import allowed_request, auth_blueprint
from src.web.controllers.Categoria import categories_blueprint
from src.web.controllers.Disciplina import disciplines_blueprint
from src.web.controllers.pagos_socio import pagos_socios_blueprint
from src.web.controllers.PerAsoc import perAsoc_blueprint
from src.web.controllers.Usuario import users_blueprint


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
        return redirect("/admin")

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html')
    
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    app.register_blueprint(perAsoc_blueprint)
    app.register_blueprint(pagos_socios_blueprint)
    app.register_blueprint(disciplines_blueprint)
    app.register_blueprint(categories_blueprint)
    app.register_blueprint(api_blueprint)


    return app    
