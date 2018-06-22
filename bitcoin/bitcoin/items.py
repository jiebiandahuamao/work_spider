# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy,time


class BitcoinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    record_timestamp = scrapy.Field()


    # def push_insert(self):
    #
    #     record_timestamp = int(time.time())
    #
    #     insert_sql ="insert into bm_spider(link,name,record_timestamp) values ('{0}','{1}',{2})"
    #     value = (self['link'],self['name'],record_timestamp)
    #     return insert_sql,value
