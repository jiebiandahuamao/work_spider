# -*- coding: utf-8 -*-
import scrapy
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from lxml import etree
from ..settings import *
from scrapy import Request
from ..items import WalianKuaixunItem
from scrapy import log

class WalianKuaixunSpider(scrapy.Spider):
    name = 'walian_kuaixun'
    # allowed_domains = ['https://www.walian.cn/live']
    start_urls = ['https://www.walian.cn/live']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{'agency_middlewares.JavaScriptMiddleware': 500},
    }

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)
        title_xpath = text.xpath('//*[@id="pane-tab0"]/ul/li/div/h4/text()')
        page = text.xpath('//*[@id="pane-tab0"]/ul/li/div/div[2]/text()')
        # 日志记录
        log_text = 'walian_kuaixun 没有抓取到数据 ' if (not title_xpath) or (not page) else 'walian_kuaixun 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in range(0, len(title_xpath)):
            print (title_xpath[i])
            print (page[i])
            self.data = self.parase_str_list(str(title_xpath[i]).replace('\n', ''), page[i])
            yield self.data

    def parase_str_list(self, title, text):
        data = WalianKuaixunItem()
        print (title)
        data['title'] = title
        data['text'] = text
        return data
