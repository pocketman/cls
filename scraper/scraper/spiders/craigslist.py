import scrapy
from scraper.items import TableItem, FlexItem

class CLSpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['example.com']
    start_urls = [
        'http://chicago.craigslist.org/search/apa',
    ]

    @staticmethod
    def set_if_not_null(mapping, key, val):
        if val:
            mapping[key] = val

    def parse_link(self, response):
        name = response.xpath('//span').extract_first()
        price = response.xpath('//span[@class="price"]/text()').extract_first()
        size = response.xpath('//span[@class="housing"]/text()').extract_first()
        location = response.xapth('').extract()


        flex_item = FlexItem()
        set_if_not_null(flex_item, 'name', name)
        yield flex_item

    def parse(self, response):
        result_links = response.xpath('//ul[@class="rows"]/li/a').css('a::attr(href)').extract()
        for result_link in result_links:
            yield scrapy.Request(
                response.urljoin(result_link),
                callback=self.parse_link,
            )

        next_page_url = response.xpath('//a[@class="button next"]').css('a::attr(href)').extract_first()
        if next_page_url is None:
            return

        yield scrapy.Request(
            response.urljoin(next_page_url),
            callback=self.parse,
            dont_filter=True,
        )