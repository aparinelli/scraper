from sqlalchemy import ForeignKey
from scraper import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.String(20), nullable = True)
    category = db.Column(db.String(20), nullable = False)
    store = db.Column(db.String(10), nullable = False)

