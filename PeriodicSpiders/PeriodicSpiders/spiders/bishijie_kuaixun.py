# -*- coding: utf-8 -*-
import scrapy
import sys
import re
# reload(sys)
# sys.setdefaultencoding('utf8')
from lxml import etree
from ..items import BishijieKuaixunItem
from scrapy import log

class BishijieKuaixunSpider(scrapy.Spider):
    name = 'bishijie_kuaixun'
    # allowed_domains = ['www.bishijie.com/kuaixun']
    start_urls = ['http://www.bishijie.com/kuaixun']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'agency_middlewares.JavaScriptMiddleware': 500},
    }

    def parse(self, response):
        body = response.body.decode(response.encoding)
        body = re.sub('<br />', '', body)
        text = etree.HTML(body)
        page_link = text.xpath("//*[@data-path_type='2']/li/h2/a/@href")
        kx_title = text.xpath("//*[@data-path_type='2']/li/h2/a/text()")
        kx_body =text.xpath("//*[@data-path_type='2']/li/div/a/text()")

        # 日志记录
        log_text = 'bishijie_kuaixun 没有抓取到数据 ' if (not kx_title) or (not kx_body) else 'bishijie_kuaixun 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        if len(kx_title) == len(kx_body):
            for i in range(0, len(kx_title)):
                print (kx_title[i])
                print (kx_body[i])  # title_xpath[i]
                print('=================================')
                self.data = self.parase_str_list(str(kx_title[i]).replace('\n', ''), kx_body[i],page_link[i])
                yield self.data

    def parase_str_list(self, title, text,page_link):
        data = BishijieKuaixunItem()
        print (title)
        data['title'] = title
        data['text'] = text.replace(' ', '')
        data['page_link'] = 'http://www.bishijie.com'+page_link
        return data
