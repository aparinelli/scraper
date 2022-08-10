import re
from scraper import app, db
from flask import jsonify, render_template, request, redirect, url_for, session
from scraper.models import Product
from scraper.models import User
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from scraper.store_spiders.spiders.jumbo_spider import JumboSpider
from scraper.store_spiders.spiders.coto_spider import CotoSpider
from scraper.store_spiders.spiders.coto_spider import url_lookup_dict

@app.route('/', methods=['GET', 'POST'])
def index():
    print(session)
    if request.method == 'POST':
        products = Product.query.all()
        return {'html': render_template('_product.html', products = products)}
    else: 
        return render_template('main.html')

@app.route('/update-database', methods=['POST'])
def update_database():
    Product.query.delete()
    global category
    for category in url_lookup_dict:
        category = category
        scrape()
        print('FINISHED SCRAPING CATEGORY ', category)
    
    products = Product.query.all()
    return {'html': render_template('_product.html', products = products)}

@app.route('/load-category', methods=['POST'])
def load_category():
    data = request.get_json()
    lookup = Product.query.filter(Product.category==data['category']).all()
    return jsonify({"alert": f"Successfully loaded {data['category']}", 'html': render_template('_product.html', products=lookup)})

@app.route('/live-search', methods=['POST'])
def live_search():
    data = request.get_json()   
    results = Product.query.filter(Product.name.contains(data['query'])).order_by(desc(Product.price)).all()
    return jsonify({'html': render_template('_product.html', products=results)})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(name = request.form['username']).first()
        if user == None:
            user = User(name = request.form['username'], password = generate_password_hash(request.form['password']))
            db.session.add(user)
            db.session.commit()

            return redirect('/')
    return render_template('register.html')

def scrape():
    global output_data
    spiders = {'Jumbo': JumboSpider, 'Coto': CotoSpider}
    

    for spider_name, spider in spiders.items():
        output_data = []
        print('CURRENT SPIDER IS ' + spider_name)
        scrape_with_crochet(spider, category = category)
        time.sleep(2)
        for x in output_data:
            product = Product(
                name = x['Producto'],
                price = x['Precio'],
                category = category,
                store = spider_name,
                img = x['Imagen']
            )
            db.session.add(product)
            db.session.commit()
        
    return jsonify(output_data)

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
import crochet

crochet.setup()
crawl_runner = CrawlerRunner()

@crochet.run_in_reactor
def scrape_with_crochet(currentSpider, category):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(currentSpider, category = category)
    return eventual

def _crawler_result(item):
    output_data.append(dict(item))
    