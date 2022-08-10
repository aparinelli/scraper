import scrapy

Soda_URL = 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&=&fq=C:/2/33/&O=OrderByScoreDESC'
Meat_URL = 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&=&fq=C:/4/55/&O=OrderByScoreDESC'
Fruits_URL = 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f3%2f48%2f221%2f&O=OrderByScoreDESC' 

class JumboSpider(scrapy.Spider):
    name = "jumbo"
    custom_settings = {"FEEDS": {"jumbo_out.json": {"format": "json", "overwrite": True}}, "CLOSESPIDER_TIMEOUT": 2}
    base_urls = []

    url_lookup_dict = {
            'Cookies': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f1%2f21%2f158%2f&O=OrderByScoreDESC',
            'Pasta': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&=&fq=C:/1/26/&O=OrderByScoreDESC',
            'Flour': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f1%2f23%2f&O=OrderByScoreDESC',
            'Oil and vinager': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f1%2f17%2f&O=OrderByScoreDESC',
            'Fruits': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f3%2f48%2f&O=OrderByScoreDESC',
            'Soda': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f2%2f33%2f&O=OrderByScoreDESC',
            'Wine': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f2%2f45%2f&O=OrderByScoreDESC',
            'Beer': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f2%2f38%2f&O=OrderByScoreDESC',
            'Juice': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f2%2f34%2f&O=OrderByScoreDESC',
            'Pork meat': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f4%2f54%2f&O=OrderByScoreDESC',
            'Beef': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f4%2f55%2f&O=OrderByScoreDESC',
            'Chicken': 'https://www.jumbo.com.ar/buscapagina?sl=1579df47-6ea5-4570-a858-8067a35362be&PS=18&cc=18&sm=0&PageNumber={}&&fq=C%3a%2f4%2f60%2f&O=OrderByScoreDESC'
        }

    category=""

    def __init__(self, category = '', **kwargs):
        self.base_urls = [self.url_lookup_dict[category]]
        super().__init__(**kwargs)

    
    def start_requests(self):
        for BASE_URL in self.base_urls:
            for n in range(1,10):
                # go through pages 1 to 9 from the given urls
                yield scrapy.Request(url=BASE_URL.format(n))

    def parse(self, response):

        list = response.xpath('//li[@layout="1579df47-6ea5-4570-a858-8067a35362be"]')
        if (list.get() is None): 
            # when it reaches the last page, there's just an empty page so list is None
            yield ' '

        else:
            for product in list: 
                name = product.xpath('.//a[@class="product-item__name"]/text()').get()
                price = product.xpath('.//span[@class="product-prices__value product-prices__value--best-price"]/text()').get()
                price = price.replace('$', '')
                price = price.replace(',', '.')

                img = product.xpath('.//a[@class="product-item__image-link"]//img/@src').extract_first()
                yield {'Producto': name, 'Precio': float(price), 'Imagen': img}

