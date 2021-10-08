import scrapy


class AuthorDetailsSpider(scrapy.Spider):
    name = 'author_details'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'test_scrapy.pipelines.StripClearItem': 400,
            'test_scrapy.pipelines.SaveAuthorDetails': 500
        }
    }

    def parse(self, response):
        for link in response.xpath("/html//div[@class='quote']/span[2]/a/@href"):
            yield scrapy.Request(url=self.start_urls[0] + link.get())
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        yield {
                "author": response.xpath("/html//div[@class='author-details']//h3/text()").get().strip(),
                "birthday": response.xpath(
                    "/html//div[@class='author-details']//span[@ class ='author-born-date']/text()"
                ).get(),
                "info": response.xpath("/html//div[@class='author-details']/div/text()").get().strip()
        }
