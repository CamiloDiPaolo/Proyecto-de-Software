from flask import Flask, request, g
from src.web.controllers.Usuario import users_blueprint
from src.web.controllers.Auth import auth_blueprint, allowed_request

def create_app():
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    @app.route("/secret")
    def secret():
        if(not allowed_request(request, ["admin"])):
            return "no tenes los permisos necesarios para acceder a este request"
        return "ruta secreta"
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    return app    