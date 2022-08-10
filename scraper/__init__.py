from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
CORS(app)
db = SQLAlchemy(app)

from scraper import views
from scraper import models
