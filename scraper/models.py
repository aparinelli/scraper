from scraper import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.String(20), nullable = True)
    category = db.Column(db.String(20), nullable = False)
    store = db.Column(db.String(10), nullable = False)
    img = db.Column(db.String(200), nullable=False)
