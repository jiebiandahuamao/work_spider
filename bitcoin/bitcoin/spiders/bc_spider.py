# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys,re
reload(sys)
sys.setdefaultencoding('utf8')

from ..items import BitcoinItem

import scrapy

from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider


class Spider(CrawlSpider):
    name = 'bc_spider'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    start_urls = ['https://coinmarketcap.com/']

    def parse(self, response):

        url = 'https://coinmarketcap.com/'
        yield scrapy.Request(url, headers=self.headers, callback=self.parse_detail)


    def parse_detail(self, response):

        img_num = re.findall('https://s2.coinmarketcap.com/static/img/coins/16x16/([0-9]{1,4}).png',response.body)
        title = response.xpath('//tbody/tr/td[2]/a/text()')
        for i in range(0,len(title)):

            self.data = self.parase_str_list(
                img_num[i],
                title[i].extract()
            )
            yield self.data

        next_urlnum = re.findall('<a href="([0-9]{1,3})">Next 100 &rarr', response.body)[0]
        print next_urlnum, "####"
        if next_urlnum:
            next_url = 'https://coinmarketcap.com/' + str(next_urlnum)
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_detail)


    def parase_str_list(self,img_num,title):
        data = BitcoinItem()
        data['link'] = "https://s2.coinmarketcap.com/static/img/coins/16x16/{}.png".format(img_num)
        data['name'] = title
        return data
