
from flask import Flask, request, redirect, render_template
from src.web.controllers.Usuario import users_blueprint
from src.web.controllers.Auth import auth_blueprint, allowed_request
from src.web.controllers.Usuario import users_blueprint
from src.web.controllers.Admin import admin_blueprint
from src.web.controllers.perAsoc import perAsoc_blueprint
from flask import Flask,render_template
from src.web.controllers.pagos import pago_blueprint
from src.web.controllers.pagos_socio import pagos_socios_blueprint

def create_app(env="development", static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

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


    return app    