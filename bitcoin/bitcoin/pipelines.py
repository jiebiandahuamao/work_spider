# -*- coding: utf-8 -*-
import time
from db_peewee import *
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import BitcoinItem
import MySQLdb

class BitcoinPipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)


    def __save_mysql(self, li):
        record_timestamp = int(time.time())
        cur = self.db.cursor()
        sql = "select count(id) from bm_spider where link = '{}' and name = '{}';".format(li['link'],li['name'])
        cur.execute(sql)
        result = cur.fetchone()
        if result[0] != 0:
            pass
        else:
            with self.db.atomic():
                # walian.insert_many(self.list).execute()
                bm_spider.insert(link=li['link'],name=li['name'],record_timestamp = record_timestamp).execute()
        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider, ):
        self.db.close()

# class BitcoinPipeline(object):
#     def __init__(self):
#         self.db = MySQLdb.connect(
#             host='localhost',
#             db="local_test",
#             user='root',
#             passwd='123456',
#             charset='utf8',
#         )

    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self.push_insert, item)
    #     query.addErrback(self.handle_error, item, spider)  # 处理异常

    # def process_item(self,item,spider):
    #     insert_sql, value = item.push_insert()
    #     cursor = self.db.cursor()
    #     sql = "select count(id) from bm_spider where link = '{}' and name = '{}';".format(value[0], value[1])
    #     cursor.execute(sql)
    #     result = cursor.fetchone()
    #     print result,"&&&&&&"
    #     if result[0] != 0:
    #         print 1111
    #         pass
    #     else:
    #         sql = insert_sql.format(value[0],value[1],value[2],)
    #         print sql,"%%%%%%%%%%%%%%%%"
    #         aa = cursor.execute(sql)
    #         print aa,"*****"
    #     # cursor.close()
    #
    # # def close_spider(self, spider, ):
    # #     self.db.close()