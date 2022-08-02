import scrapy
url_lookup_dict = {
        'Galletitas': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-panaderia-galletitas/_/N-10z239c?Dy=1&Nf=product.endDate%7CGTEQ%2B1.6587072E12%7C%7Cproduct.startDate%7CLTEQ%2B1.6587072E12&Nr=AND(product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR(product.siteId%3ACotoDigital))'],
        'Cereales': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-cereales/_/N-ukd5id'],
        'Pastas': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-pasta-seca-lista-y-rellenas/_/N-tvb9c7'],
        'Harinas': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-harinas/_/N-842qrm'],
        'Aceites y vinagres': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-aceites-y-condimentos/_/N-18r69ct'],
        'Frutas': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-frutas-y-verduras-frutas/_/N-1edtocx?Nf=product.endDate%7CGTEQ+1.6570656E12%7C%7Cproduct.startDate%7CLTEQ+1.6566336E12%7C%7Cproduct.startDate%7CLTEQ+1.6570656E12%7C%7Cproduct.endDate%7CGTEQ+1.6566336E12&No=0&Nr=AND%28product.language%3Aespa%C3%B1ol%2Cproduct.sDisp_200%3A1004%2COR%28product.siteId%3ACotoDigital%29%29&Nrpp=48'],
        'Verduras': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-frutas-y-verduras-verduras/_/N-1vh8n7u;jsessionid=XHBfRbtH1Zyt-9fH7a-foICp1vXfMp1P3NXxjJhrZulN8OgXvLHy!1129442141!-269144473?Nf=product.endDate%7CGTEQ+1.6593984E12%7C%7Cproduct.startDate%7CLTEQ+1.6593984E12&Nr=AND%28product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR%28product.siteId%3ACotoDigital%29%29'],
        'Gaseosas': ['http://api.cotodigital.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-gaseosas/_/N-n4l4r5'],
        'Vinos': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-con-alcohol-vinos/_/N-uqiqtm'],
        'Cervezas': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-con-alcohol-cerveza/_/N-137sk0z'],
        'Jugos': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-jugos/_/N-11la5tu'],
        'Carne vacuna': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-carniceria-carnes/_/N-1uhue0v'],
        'Pollo': ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-aves/_/N-6drhk5'] 
    }

class CotoSpider(scrapy.Spider):
    name = 'coto'
    start_urls = []

    custom_settings = {"FEEDS": {"coto_out.json": {"format": "json", "overwrite": True}}, "CLOSESPIDER_TIMEOUT": 15}

    
    def __init__(self, category='', **kwargs):
        self.start_urls = url_lookup_dict[category]
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
        

