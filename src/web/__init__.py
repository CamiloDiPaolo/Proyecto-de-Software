from flask import Flask
from src.web.controllers.Foo import foo_blueprint

def create_app():
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    app.register_blueprint(foo_blueprint)

    return app    