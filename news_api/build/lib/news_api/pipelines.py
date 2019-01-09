# -*- coding: utf-8 -*-
import time
from db_peewee import *
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FlaskApiPipeline(object):

    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)

    def __save_mysql(self, li):
        record_timestamp = int(time.time())
        cur = self.db.cursor()
        sql = "select count(id) from get_news_api where id = %s;"
        cur.execute(sql, (li['id']))
        result = cur.fetchone()
        if result[0] != 0:
            pass
        else:
            with self.db.atomic():
                # walian.insert_many(self.list).execute()
                get_news_api.insert(id = li['id'],content=li['content'],title=li['title'], timel=li['timel'],record_timestamp = record_timestamp).execute()
        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider, ):
        self.db.close()