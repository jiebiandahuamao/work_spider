# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import sys
import re
# reload(sys)
# sys.setdefaultencoding('utf8')
from lxml import etree
from ..settings import *
from ..items import HistoricalDataItem
from scrapy import Request
import time
import datetime
import MySQLdb
from scrapy import log

class HistoricalDataSpider(scrapy.Spider):
    name = 'historical_data'
    # allowed_domains = ['https://coinmarketcap.com']
    # start_urls = ['https://coinmarketcap.com/']

    def start_requests(self):
        start_url_request_list = []
        db = MySQLdb.connect(host="218.244.138.88",port=13456, db="spiderdb", user="spiderdb", passwd="Cqmyg321", charset='utf8')
        cursor = db.cursor()
        sql = "select currency_id from t_currency_main_temp"
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()

        if results:
            self.name_list= [i[0] for i in results]
        else:
            self.name_list = ['bitcoin','ethereum','ripple','bitcoin-cash','eos','cardano','litecoin','stellar','tron','neo']
        self.run_time = 0
        self.a = []
        in_time = datetime.date.today() - datetime.timedelta(days=2)
        start_time = str(in_time).replace('-', '')
        while self.run_time < len(self.name_list):
            url = 'https://coinmarketcap.com/zh/currencies/' + self.name_list[self.run_time] +'/historical-data/?start={}&end=20281229'.format(start_time)
            self.run_time +=1
            yield Request(url, callback=self.parse)

    def parse(self, response):
        body1 = str(response.body)          #.decode(response.encoding, 'ignore')
        body = re.sub(r',', '', body1)
        currency_id = re.findall(r'https://coinmarketcap.com/zh/currencies/(.*)/historical-data', response.url)[0]
        text = etree.HTML(body)
        timestamp = response.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[1]/text()')
        open_price = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[2]/text()')
        high_price = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[3]/text()')
        low_price = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[4]/text()')
        close_price = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[5]/text()')
        turnover_volume = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[6]/text()')
        marke_value = text.xpath('//*[@class="table-responsive"]/table/tbody/tr/td[7]/text()')
        unit = 'USD'
        for i in timestamp:
            print (i,333333333333333)
        # 日志记录
        log_text = 'historical_data 没有抓取到数据 ' if (not currency_id) or (not timestamp) else 'historical_data 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in range(len(timestamp)):
            self.data = self.parase_str_list(currency_id,timestamp[i],open_price[i],high_price[i],low_price[i],close_price[i],turnover_volume[i],marke_value[i],unit)
            yield self.data
    def parase_str_list(self,currency_id,timestamp,open_price,high_price,low_price,close_price,turnover_volume,marke_value,unit):
        data = HistoricalDataItem()
        timestamp1 = re.search(u"(\d+)年(\d+)月(\d+)日",str(timestamp))
        time_change = timestamp1.group(1) + '-' + timestamp1.group(2) + '-' + timestamp1.group(3)
        time1 = time.strptime(time_change, '%Y-%m-%d')
        publish_timestamp = int(time.mktime(time1))
        data['currency_id'] = currency_id
        data['publish_timestamp'] = int(publish_timestamp)
        data['open_price'] = float(open_price)
        data['high_price'] = float(high_price)
        data['low_price'] = float(low_price)
        data['close_price'] = float(close_price)
        if turnover_volume == '-':
            data['turnover_volume'] = None
        else:
            data['turnover_volume'] = int(turnover_volume)
        if marke_value == '-':
            data['marke_value'] = None
        else:
            data['marke_value'] = int(marke_value)
        data['unit'] = unit
        return data
