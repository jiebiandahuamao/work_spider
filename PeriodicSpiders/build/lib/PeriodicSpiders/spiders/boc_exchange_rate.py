# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from ..settings import *
from scrapy import Request
from ..items import BocExchangeRateItem
from scrapy import log


class BocExchangeRateSpider(scrapy.Spider):
    name = 'boc_exchange_rate'
    # allowed_domains = ['data.bank.hexun.com']
    start_urls = ['http://data.bank.hexun.com/']

    def parse(self, response):

        url = 'http://data.bank.hexun.com/other/cms/foreignexchangejson.ashx?callback=ShowDatalist'
        yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        body = response.body.decode("GBK","ignore")
        text = etree.HTML(body)
        print(type(body),body,"&&&&&")
        all_tate = re.findall("{bank:'中国银行',currency:'(美元|日元|欧元|英镑|澳大利亚元|加拿大元|瑞士法郎|港币|新台币|韩元|泰国铢|澳门元|林吉特|卢布|南非兰特|新西兰元|菲律宾比索|新加坡元|瑞典克朗|丹麦克朗|挪威克朗)',code:'([A-Z]*)',currencyUnit:'.*?',cenPrice:'(.*?)',",body)
        hk_cny_rate = z = re.findall("{bank:'中国银行',currency:'(港币)',code:'([A-Z]*)',currencyUnit:'.*?',cenPrice:'(.*?)',", body)
        cny_100hk_rate = 1 / float(hk_cny_rate[0][2])

        # 日志记录
        log_text = 'walian 没有抓取到数据 ' if (not all_tate) or (not hk_cny_rate) else 'walian 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in all_tate:
            li = list(i)
            if i[0] == '港币':
                cn_name = '人民币'
                en_name = 'CNY'
                exchange_rate = cny_100hk_rate*100
                self.data = self.parase_str_list(cn_name, en_name, exchange_rate)
            else:
                cn_name = li[0]
                en_name = li[1]
                exchange_rate = cny_100hk_rate*float(li[2])
                self.data = self.parase_str_list(cn_name, en_name, exchange_rate)
            yield self.data

    def parase_str_list(self,cn_name,en_name,exchange_rate):
        data = BocExchangeRateItem()
        code = self.code(en_name)
        data['code'] = code
        data['cn_name'] = cn_name
        data['en_name'] = en_name
        data['exchange_rate'] = exchange_rate
        return data

    def code(self, en_name):
        if en_name == 'USD':
            code = 1000
            return code
        if en_name == 'CNY':
            code = 1420
            return code
        if en_name == 'JPY':
            code = 1160
            return code
        if en_name == 'MOP':
            code = 1210
            return code
        if en_name == 'MYR':
            code = 1220
            return code
        if en_name == 'SGD':
            code = 1320
            return code
        if en_name == 'CNY':
            code = 1420
            return code
        if en_name == 'TWD':
            code = 1430
            return code
        if en_name == 'EUR':
            code = 3000
            return code
        if en_name == 'GBP':
            code = 3030
            return code
        if en_name == 'CAD':
            code = 5010
            return code
        if en_name == 'AUD':
            code = 6010
            return code
        if en_name == 'PHP':
            code = 1290
            return code
        if en_name == 'KRW':
            code = 1330
            return code
        if en_name == 'THB':
            code = 1360
            return code
        if en_name == 'DKK':
            code = 3020
            return code
        if en_name == 'NOK':
            code = 3260
            return code
        if en_name == 'SEK':
            code = 3300
            return code
        if en_name == 'CHF':
            code = 3310
            return code
        if en_name == 'NZD':
            code = 6090
            return code
        if en_name == 'ZAR':
            code = 7113
            return code
        if en_name == 'RUB':
            code = 3440
            return code