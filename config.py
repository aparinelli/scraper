from os import environ, path
from dotenv import load_dotenv

basedir=path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config:
    FLASK_APP=environ.get("FLASK_APP")
    FLASK_ENV=environ.get("FLASK_ENV")
    SECRET_KEY=environ.get("FLASK_ENV")

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"