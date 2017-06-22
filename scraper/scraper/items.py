# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from collections import defaultdict
from scrapy.loader.processors import TakeFirst, MapCompose
from scraper.utils import striphtmlandnonunicode

class TableItem(scrapy.Item):
  """An Item that creates fields dynamically"""
  fields = defaultdict(scrapy.Field)

  def __init__(self, thead_selector, trow_selector):
    headers = thead_selector.xpath('.//tr/th/text()').extract()
    values = trow_selector.xpath('.//td').extract()
    self._values = defaultdict(
      scrapy.Field,
      zip(
        [str(x).lower().strip().replace(" ", "_").replace(",", "") for x in headers],
        [str(striphtmlandnonunicode(x)).lower().strip() for x in values]
      )
    )

class FlexItem(scrapy.Item):
  """An Item with dynamic fields"""
  fields = defaultdict(scrapy.Field)
