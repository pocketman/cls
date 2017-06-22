import scrapy
from scraper.items import TableItem, FlexItem
from scraper.utils import striphtmlandnonunicode

class CLSpider(scrapy.Spider):
  name = 'proxy'
  allowed_domains = ['example.com']
  start_urls = [
    'http://chicago.craigslist.org/search/apa',
    'http://sfbay.craigslist.org/search/apa',
  ]

  @staticmethod
  def set_if_not_null(mapping, key, val):
    if val:
      mapping[key] = val

  @staticmethod
  def parse_attributes(response):
    return []

  def parse_link(self, response):
    name = response.xpath('//span').extract_first()
    price = response.xpath('//span[@class="price"]/text()').extract_first()
    size = response.xpath('//span[@class="housing"]/text()').extract_first()
    lat = float(response.xpath('//div[@id="map"]').css('::attr(data-latitude)').extract_first())
    lon = float(response.xpath('//div[@id="map"]').css('::attr(data-longitude)').extract_first())
    location = response.xapth('//div[@class="mapaddress"]/text()').extract_first()
    title = response.xpath('//span[@id="titletextonly"]/text()').extract_first()
    attributes = parse_attributes(response)
    description = '
    n'.join(response.xpath('//section[@id="postingbody"]/text()').extract()

    flex_item = FlexItem()
    set_if_not_null(flex_item, 'name', name)
    set_if_not_null(flex_item, 'price', price)
    set_if_not_null(flex_item, 'size', size)
    set_if_not_null(flex_item, 'location', location)
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
