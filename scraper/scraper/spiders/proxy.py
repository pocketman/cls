import scrapy
from scraper.items import TableItem

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['example.com']
    start_urls = [
        'https://incloak.com/proxy-list/?country=DEGBUS&anon=34#list',
    ]

    def parse(self, response):
        thead_selector = response.xpath('//thead')
        if len(thead_selector) == 0:
            raise StopIteration

        for tr in response.xpath('//tbody/tr'):
            yield TableItem(thead_selector, tr)

        next_page_url = response.xpath(
                '//li[@class="arrow__right"]/a').css('a::attr(href)'
            ).extract_first()
        if next_page_url is None:
            return

        yield scrapy.Request(
            response.urljoin(next_page_url),
            callback=self.parse,
            dont_filter=True,
        )