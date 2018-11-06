# -*- coding: utf-8 -*-
# from __future__ import print_function
import _strptime
import oss2
import sys
import os
from scrapy.utils.project import get_project_settings
import datetime
import threading
import time
import scrapy
from scrapy import log

class OSSMiddleWares(object):

    def __init__(self):
        settings = get_project_settings()
        self.WEB_PAGE_ENCODING = settings.get('WEB_PAGE_ENCODING')
        print (self.WEB_PAGE_ENCODING)


    def process_spider_input(self,response,spider):
        url = str(response.url)
        body = (response.body).decode(self.WEB_PAGE_ENCODING,'ignore')
        put_oss_thread = OSSMiddleWares.OSSThread(url,body)
        put_oss_thread.start()
        return None

    class OSSThread(threading.Thread):  # 继承父类threading.Thread
        def __init__(self, url,body):
            settings = get_project_settings()
            threading.Thread.__init__(self)
            self.url = url
            self.body = body
            self.OSS_ACCESS_KEY_ID = settings.get('OSS_ACCESS_KEY_ID')
            self.OSS_ACCESS_KEY_SECRET = settings.get('OSS_ACCESS_KEY_SECRET')
            self.OSS_ENDPOINT = settings.get('OSS_ENDPOINT')
            self.OSS_BUCKET = settings.get('OSS_BUCKET')
            self.spider_name = settings.get('BOT_NAME')
            print (self.OSS_ACCESS_KEY_ID)
            print (self.OSS_ACCESS_KEY_SECRET)
            print (self.OSS_ENDPOINT)
            print (self.OSS_BUCKET)
            print (self.spider_name)

        def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
            if os.path.split(os.getcwd())[-1]:
                # spider_name = os.path.split(os.getcwd())[-1]
                record_date, record_time = self.__get_time()
                oss_url = self.url.replace('/', '{:}')
                # file_name = 'source' + '/' + spider_name + '/' + record_date + '/' + oss_url + ' = ' + record_time
                file_name = 'ceshi' + '/' + self.spider_name + '/' + datetime.datetime.now().strftime('%Y-%m') + '/' + datetime.datetime.now().strftime('%d') + '/' + record_time
                # file_name = 'source' + '/' + self.spider_name + '/' + datetime.datetime.now().strftime('%Y-%m') + '/' + datetime.datetime.now().strftime('%d') + '/' + record_time
                auth = oss2.Auth(self.OSS_ACCESS_KEY_ID,self.OSS_ACCESS_KEY_SECRET)

                def percentage(consumed_bytes, total_bytes):
                    if total_bytes:
                        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                        # print '\r{0}  {1}% '.format(self.url,rate)
                        scrapy.log.msg('\r{0}  {1}% '.format(self.url,rate), level=log.INFO )
                        sys.stdout.flush()
                try:
                    bucket = oss2.Bucket(auth, self.OSS_ENDPOINT ,self.OSS_BUCKET)
                    bucket.put_object(file_name, self.body, progress_callback=percentage)
                    # print ('finish_put_oss' + ': ' + self.url)
                    scrapy.log.msg('finish_put_oss' + ': ' + self.url, level=log.INFO )

                except:
                    scrapy.log.msg(self.url+'OSS_ERROR', level=log.ERROR )

        def __get_time(self):
            localtime = time.localtime()
            year = str(localtime.tm_year)
            mon = str(localtime.tm_mon)
            day = str(localtime.tm_mday)
            hour = str(localtime.tm_hour)
            min = str(localtime.tm_min)
            sec = str(localtime.tm_sec)

            record_date = year + '-' + mon + '-' + day
            record_time = hour + '-' + min + '-' + sec
            return record_date, record_time