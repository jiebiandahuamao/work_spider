# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys,re
reload(sys)
sys.setdefaultencoding('utf8')

from ..items import NewsApiItem

import scrapy

from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider


class Spider(CrawlSpider):
    name = 'get_news_api'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        url = 'http://114.215.177.242:7777/'
        yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):

        id = response.xpath("//doc/docid/text()")
        content = re.findall('<dochtmlcontent><!\[CDATA\[<div class=TRS_Editor><p align="justify">(.*?)</dochtmlcontent>', response.body)
        title = re.findall('<doctitle>(.*?)</doctitle>', response.body)
        timel = response.xpath("//doc/docfirstpubtime/text()")


        for i in range(0,len(id)):

            id[i] = id[i].extract().replace(' ', '').replace('\\n', '')
            content[i] = re.sub(r'<strong>|</strong>|<p>|</p>|<p align="center">|<p align="justify">|', "", content[i])
            title[i] = title[i].replace('<![CDATA[', '').replace(']]>', '')
            timel[i] = timel[i].extract().replace(' ', '')

            self.data = self.parase_str_list(
                id[i],
                content[i],
                title[i],
                timel[i])
            yield self.data if content[i].startswith('FX') else None

    def parase_str_list(self, id,content,title,timel):
        data = NewsApiItem()
        data['id'] = id
        data['content'] = content
        data['title'] = title
        data['timel'] = timel

        return data
