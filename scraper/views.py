import re
from scraper import app, db
from flask import jsonify, render_template, request, redirect, url_for, session
from scraper.models import Product
from scraper.models import User
from sqlalchemy import desc

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

@app.route('/get-categories', methods=['POST'])
def get_categories():
    return jsonify(url_lookup_dict)

@app.route('/delete-database', methods=['POST'])
def delete_database():
    Product.query.delete()
    return {'alert': 'Success.'}

@app.route('/update-database', methods=['POST'])
def update_database():
    global category
    category = request.get_json()['category']
    Product.query.filter(Product.category==category).delete()
    db.session.commit()
    scrape()
    products = Product.query.filter(Product.category==category).all()
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

def scrape():
    global output_data
    spiders = {'Jumbo': JumboSpider, 'Coto': CotoSpider}
    

    for spider_name, spider in spiders.items():
        output_data = []
        scrape_with_crochet(spider, category = category)
        time.sleep(3)
        print('CURRENT SPIDER IS ' + spider_name)
        print('CURRENT CATEGORY IS ' + category)
        print(output_data)
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
    