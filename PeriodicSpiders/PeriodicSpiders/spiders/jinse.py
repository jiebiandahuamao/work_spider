# -*- coding: utf-8 -*-
import scrapy
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from lxml import etree
from ..settings import *
from scrapy import Request
from ..items import JinseItem
from scrapy import log

class JinseSpider(scrapy.Spider):

    name = 'jinse'
    # allowed_domains = ['www.jinse.com/xinwen']
    start_urls = ['http://www.jinse.com/xinwen']

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)
        urls = text.xpath('//*[@id="app"]//ul/h3/a/@href')
        for i in urls:
            yield Request(i, callback=self.parse_detail)

    def parse_detail(self,response):
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)
        title_xpath = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/h2/text()')
        page = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/p[not(@style="text-align: center;")]/text()')
        page_link = response.url
        # 日志记录
        log_text = 'jinse 没有抓取到数据 ' if (not title_xpath) or (not page) else 'jinse 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in range(0,len(title_xpath)):
            for z in page:
                news_text.append(z)
            news_text1 = "".join(news_text)
            self.data = self.parase_str_list(title_xpath[i],news_text1,page_link)
            return self.data

    def parase_str_list(self, title,text,page_link):
        data = JinseItem()
        data['title'] = title
        data['text'] = text
        data['page_link'] = page_link
        return data
