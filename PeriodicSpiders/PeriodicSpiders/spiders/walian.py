# -*- coding: utf-8 -*-
import scrapy
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from lxml import etree
from ..settings import *
from scrapy import Request
from ..items import WalianItem
from scrapy import log

class WalianSpider(scrapy.Spider):
    name = 'walian'
    # allowed_domains = ['http://www.walian.cn']
    start_urls = ['https://www.walian.cn/']

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)
        urls = text.xpath('//div[@class="el-tabs__content"]/div[2]/div/div/a/@href')
        for i in urls:
            url = 'https://www.walian.cn' + i
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)
        page_link = response.url
        title_xpath = text.xpath('//*[@id="app"]/main/div/div/div[2]/div[2]/text()')
        page = text.xpath('//*[@id="app"]/main/div/div/div[2]/div[4]//p//text()')

        #日志记录
        log_text = 'walian 没有抓取到数据 'if (not title_xpath)or (not page) else 'walian 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in range(0,len(title_xpath)):
            for z in page:
                news_text.append(z)
            news_text1 = "".join(news_text)
            self.data = self.parase_str_list(str(title_xpath[i]).replace('\n',''),news_text1,page_link)
            return self.data

    def parase_str_list(self, title, text,page_link):
        data = WalianItem()
        data['title'] = title
        data['text'] = text
        data['page_link'] = page_link
        return data
