# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String
# from src.web.config import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_session = db.session
Base = db.Model

def init_app(app):
    db.init_app(app)





# engine = create_engine(config["development"].SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()


# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     Base.metadata.create_all(bind=engine)

