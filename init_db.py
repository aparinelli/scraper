import os
DATABASE_PATH = '/Users/alejoparinelli/Desktop/scraper/scraper/database.db'

if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)    
from scraper import db
db.create_all()