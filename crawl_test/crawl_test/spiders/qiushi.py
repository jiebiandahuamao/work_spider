# -*- coding: utf-8 -*-
import scrapy,sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawl_test.items import CrawlTestItem
from lxml import etree
from ..settings import *
reload(sys)
sys.setdefaultencoding('utf8')




class QiushiSpider(CrawlSpider):
    name = 'qiushi'
    allowed_domains = ['www.jinse.com']
    start_urls = ['https://www.jinse.com']

    rules = (
        Rule(LinkExtractor(allow=(r'bitcoin/\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=(r'news/bitcoin/\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=(r'blockchain/\d+.html',)), callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        item = CrawlTestItem()
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING, 'ignore')).encode('utf8')
        text = etree.HTML(body)

        title_xpath = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/h2/text()')
        page = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/p[not(@style="text-align: center;")]/text()')

        for i in range(0,len(title_xpath)):
            for z in page:
                news_text.append(z)
            news_text1 = "".join(news_text)
            self.data = self.parase_str_list(title_xpath[i],news_text1)
            return self.data

    def parase_str_list(self, title, text):
        data = CrawlTestItem()
        data['title'] = title
        data['text'] = text
        return data
