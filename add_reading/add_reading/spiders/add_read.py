# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from scrapy import log
from scrapy.exceptions import CloseSpider
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import re
from lxml import etree


class JobbleSpider(RedisSpider):
    name = 'add_read'

    def __init__(self, url=None, time=None, ENABLE_PROXY=None, *args, **kwargs):
        self.i = 0
        self.URL = url
        self.RUN_TIME = time
        self.ENABLE_PROXY = ENABLE_PROXY

    def start_requests(self):
        start_url_request_list = []
        i = 1

        while i <= int(self.RUN_TIME) * 1.25:
            url = self.URL

            start_request = Request(url, callback=self.parse,dont_filter=True)  # ,headers={'Referer':http://www.example.com/'}),headers = self.headers不断开和关
            start_url_request_list.append(start_request)
            i += 1
        scrapy.log.msg("预计刷 :" + str(self.RUN_TIME), level=log.WARNING)
        return start_url_request_list


    def parse(self, response):
        print response.url
        # 财富
        if "caifuhao.eastmoney.com" in response.url:
            readcount = response.xpath('//*[@id="readcount"]/text()')
            self.judge_pv(readcount, response.url)
        # 财富移动版
        if "emcreative.eastmoney.com" in response.url:
            readcount = response.xpath('//html/body/div[2]/div[2]/p/text()')
            self.judge_pv(readcount, response.url)
        # 中金
        elif "mp.cnfol.com" in response.url:
            readcount = response.xpath('//html/body/div[3]/div[1]/div[3]/div/div[1]/span[2]/text()')
            print readcount,"*************&&&&&&&&&&&&&"
            self.judge_pv(readcount ,response.url)
        # 格隆汇网页
        elif "www.gelonghui.com" in response.url:
            readcount = response.xpath('//*[@id="content"]/div/div/div[1]/div[1]/div[2]/p[2]/span[1]/em[1]/text()')
            self.judge_pv(readcount, response.url)
        # 格隆汇移动版
        elif "m.gelonghui.com" in response.url:
            readcount = response.xpath('/html/body/section/div[1]/div[1]/span/text()')
            self.judge_pv(readcount, response.url)
        # 格隆汇column/article/
        elif "www.gelonghui.com" in response.url:
            readcount = response.xpath('//*[@id="main"]/div[2]/div[1]/span[2]/text()')
            self.judge_pv(readcount, response.url)
        # 搜狐
        elif "www.sohu.com" in response.url:
            get_readcount = requests.get('http://v2.sohu.com/public-api/articles/239178870/pv?callback=jQuery112408078212816495984_1530690868131&_=1530690868132')
            readcount = re.search("\((\d+)\)",get_readcount.text).group(1)
            # readcount = response.xpath('//*[@id="article-container"]/div[2]/div[1]/div[3]/div[1]/span/em/text()')
            self.judge_pv(readcount, response.url)
        # 搜狐移动版
        elif "m.sohu.com" in response.url:
            readcount = response.xpath('//html/body/div[3]/div[3]/article/div/span/em/text()')
            self.judge_pv(readcount, response.url)


    def judge_pv(self,readcount,url):
        if readcount:
            if isinstance(readcount,unicode):
                i = readcount
                print i,"***********************************8"
            else:
                i = readcount[0].extract()
            i = str(i).replace('阅读 ', '').replace(u'阅读：','')
            if "万" in i:
                views = str(i).replace('万', '')
                run_time = float(self.RUN_TIME) / 10000
                scrapy.log.msg(views + "万 :预计刷" + str(run_time) + "万" , level=log.WARNING)
                if float(views) >= run_time:
                    raise CloseSpider(views + '万 完成')
            elif int(i) == 0:
                raise Exception("PV==0")
            else:
                # print i, self.RUN_TIME
                scrapy.log.msg(i + " :" + str(self.RUN_TIME), level=log.WARNING)
                if int(i) > int(self.RUN_TIME):
                    raise CloseSpider( '完成  ' + str(i) +  '  ' + url )
        else:
            self.i += 1
            scrapy.log.msg(" PV==None次数:" + str(self.i), level=log.WARNING)
            if self.i > 2:
                self.i = 0
                raise Exception("PV==None")

