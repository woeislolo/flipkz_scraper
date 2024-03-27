import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from flip_kz.items import Book


class BookSpider(CrawlSpider):
    ''' Выбирает ссылки c сайта flip.kz из категории Книги/Автомобили, 
    оставляет товары (allow='catalog\?prod') с id=content '''
    
    name = 'books'
    allowed_domains = ['flip.kz']
    start_urls = ['https://www.flip.kz/catalog?subsection=50']
    rules = [Rule(LinkExtractor(allow='catalog\?prod', restrict_css='#content'), 
                  callback='parse_items', 
                  )]


    def parse_items(self, response):
        book = Book()
        book['title'] = response.xpath('//td[2]/h1//text()').get()
        book['author'] = response.xpath('//td[2]/p/a//text()').get()
        book['url'] = response.url
        return book
