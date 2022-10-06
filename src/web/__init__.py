from flask import Flask,render_template
from src.web.controllers.pagos import pago_blueprint
from src.web.controllers.pagos_socio import pagos_socios_blueprint

def create_app():
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return render_template("admin.html")

    app.register_blueprint(pago_blueprint)
    app.register_blueprint(pagos_socios_blueprint)

    return app    