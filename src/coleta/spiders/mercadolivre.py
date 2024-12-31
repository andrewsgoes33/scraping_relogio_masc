import scrapy
from datetime import datetime


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/relogio-masculino"]
    page_count = 1
    max_pages = 10
    
    def parse(self, response):
        
        products = response.css('div.poly-card__content')
        
        for product in products:
        
            Price_Reais = product.css('span.andes-money-amount__fraction::text').getall()
            Price_Cents = product.css('span.andes-money-amount__cents::text').getall() 
            
            yield {'Marketplace' : 'Mercado Livre',
                    'Category' : 'Joias e Relógios > Relógios > De Pulso',
                    'Brand' : product.css('span.poly-component__brand::text').get(),
                    'Name' : product.css('h2.poly-box.poly-component__title a::text').get(),
                    'Old_Price_Reais' : Price_Reais[0] if len(Price_Reais) > 0 else None,
                    'Old_Price_Cents' : Price_Cents[0] if len(Price_Cents) > 0 else None,
                    'New_Price_Reais' : Price_Reais[1] if len(Price_Reais) > 1 else None,
                    'New_Price_Cents':  Price_Cents[1] if len(Price_Cents) > 1 else None,
                    'Reviews_Rating' : product.css('span.poly-reviews__rating::text').get(),
                    'Reviews_Total' : product.css('span.poly-reviews__total::text').get(),
                    'Ad_Link' : product.css('h2.poly-box.poly-component__title a::attr(href)').get(),
                    'Extraction_Date' : datetime.now()
                    }

        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
            