import json
from math import prod
from nis import match
from unicodedata import category
import uuid

from numpy import mat
from scraper import app, db
from flask import jsonify, render_template, request, redirect, url_for
from scraper.models import Product

from scraper.store_spiders.spiders.jumbo_spider import JumboSpider
from scraper.store_spiders.spiders.coto_spider import CotoSpider

@app.route('/')
def index():
    products = Product.query.all()
    if products == []:
        
        products = Product.query.all()

    return render_template('index.html')

@app.route('/load-category', methods=['POST'])
def load_category():
    data = request.get_json()
    lookup = Product.query.filter(Product.category == data['category']).first()

    if (lookup == None):
        scrape(data['category'])
        return jsonify({"alert": f"Successfully loaded {data['category']}"})
    else:
        return jsonify({"alert": f"{data['category']} is already in database"})

@app.route('/live-search', methods=['POST'])
def live_search():
    data = request.get_json()   
    results = Product.query.filter(Product.name.contains(data['query'])).distinct()
    print(data['query'], results)
    return jsonify({'html': render_template('_product.html', products=results)})

def scrape(category):
    global output_data
    spiders = {'Jumbo': JumboSpider, 'Coto': CotoSpider}
    

    for spider_name, spider in spiders.items():
        output_data = []
        print('CURRENT SPIDER IS ' + spider_name)
        scrape_with_crochet(spider, category = category)
        time.sleep(10)
        print(output_data)
        for x in output_data:
            product = Product(
                name = x['Producto'],
                price = x['Precio'],
                category = category,
                store = spider_name
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