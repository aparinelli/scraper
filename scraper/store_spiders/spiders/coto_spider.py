from posixpath import abspath
import scrapy
import json
from os.path import dirname

FILE_PATH = dirname(abspath(__file__)) + '/url_lookup_coto.json'
with open(FILE_PATH, 'r') as f:
    url_lookup_dict = json.load(f)

class CotoSpider(scrapy.Spider):
    name = 'coto'
    start_urls = []

    custom_settings = {"FEEDS": {"coto_out.json": {"format": "json", "overwrite": True}}, "CLOSESPIDER_TIMEOUT": 2}

    
    def __init__(self, category='', **kwargs):
        self.start_urls = [url_lookup_dict[category]]
        super().__init__(**kwargs)

    def parse(self, response):
        pagination = response.xpath('//div[@class="atg_store_pagination"]')
        next_page_list = pagination.css('a ::attr(href)').extract()

        base_url = 'https://www.cotodigital3.com.ar'
        
        url_list = [response.url]

        for next_page in next_page_list:
            url_list.append(base_url + next_page)
        
        for url in url_list:
            yield scrapy.Request(url, callback = self.parse_products)

    def parse_products(self, response):
        list = response.xpath('//li[contains(@id, "li_prod")]')
        for product in list:
            name = product.xpath('.//div[@class="descrip_full"]/text()').get()
            price = product.xpath('.//span[@class="atg_store_newPrice"]/text()').extract()
            price[1] = price[1].replace('\n', '')
            price[1] = price[1].replace('\t', '')
            price[1] = price[1].replace(' ', '')
            price[1] = price[1].replace('$', '')
            price[1] = price[1].replace(',', '.')

            img = product.xpath('.//span[@class="atg_store_productImage"]//img/@src').extract_first()
            yield {'Producto': name, 'Precio': float(price[1]), 'Imagen': img}
        

