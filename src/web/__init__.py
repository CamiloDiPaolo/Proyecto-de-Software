from flask import Flask, request, redirect, render_template
from src.web.controllers.Usuario import users_blueprint
from src.web.controllers.Auth import auth_blueprint, allowed_request
from src.web.controllers.Usuario import users_blueprint

def create_app():
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    @app.route("/admin", methods=["GET"])
    def admin():
        if(not allowed_request(request, ["admin"])):
            return redirect("/auth/login")
        return render_template('admin.html')

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    return app    