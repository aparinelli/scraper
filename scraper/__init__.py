from distutils.command.config import config
from unicodedata import category
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from hyperlink import register_scheme

app = Flask(__name__)
app.config["SECRET_KEY"] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
CORS(app)
db = SQLAlchemy(app)

app.config.from_object('config.Config')

from scraper import views
from scraper import models

