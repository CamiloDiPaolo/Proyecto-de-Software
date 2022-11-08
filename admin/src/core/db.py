from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_session = db.session
Base = db.Model

def init_app(app):
    db.init_app(app)



