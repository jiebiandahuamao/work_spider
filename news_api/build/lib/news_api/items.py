# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsApiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    timel = scrapy.Field()
    record_timestamp = scrapy.Field()
    pass
