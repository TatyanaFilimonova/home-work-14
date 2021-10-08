import scrapy
from ..pgdb import pgsession
from ..SQLalchemy_classes import *


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'test_scrapy.pipelines.DeleteQuotes': 100,
            'test_scrapy.pipelines.DeleteNewLine': 200,
            'test_scrapy.pipelines.SaveToPostgres': 300
        }
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):

            yield {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get(),
                "link": self.start_urls[0]+quote.xpath("span/a/@href").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
