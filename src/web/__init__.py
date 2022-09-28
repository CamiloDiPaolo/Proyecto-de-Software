from flask import Flask,render_template
from src.web.controllers.pagos import pago_blueprint

def create_app():
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    app.register_blueprint(pago_blueprint)

    return app    