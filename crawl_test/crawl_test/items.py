# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import time
import scrapy


class CrawlTestItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    text = scrapy.Field()
    record_timestamp = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into crawl_test(title,text,record_timestamp) values (%s,%s,%s)
        """
        record_timestamp = int(time.time())
        params = (self['title'],self['text'], record_timestamp)

        return insert_sql,params