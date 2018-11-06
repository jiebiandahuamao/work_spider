# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from lxml import etree
import time
from ..items import BitcoinMarketsItem
from scrapy import log


class BitcoinMarketsSpider(scrapy.Spider):
    name = 'bitcoin_markets'
    # allowed_domains = ['https://coinmarketcap.com']
    # start_urls = ['https://coinmarketcap.com/']

    def start_requests(self):
        self.name_list = ['bitcoin','ethereum','ripple','bitcoin-cash','eos','cardano','litecoin','stellar','tron','neo']
        self.run_time = 0
        self.a = []
        while self.run_time < 10:
            url = 'https://coinmarketcap.com/currencies/' + self.name_list[self.run_time] +'/#markets'
            self.run_time +=1
            yield Request(url, callback=self.parse,dont_filter=True)

    def parse(self, response):

        body = response.body.decode(response.encoding)
        body = re.sub(r'<br />|\n|\$|,', '', body)
        text = etree.HTML(body)
        market = text.xpath('//*[@id="markets-table"]/tbody/tr/td[2]/a/text()')
        unit = text.xpath('//*[@id="markets-table"]/tbody/tr/td[3]/a/text()')
        volume_24h = text.xpath('//*[@id="markets-table"]/tbody/tr/td[4]/span/text()')
        price = text.xpath('//*[@id="markets-table"]/tbody/tr/td[5]/span/text()')
        valume_rate = text.xpath('//*[@id="markets-table"]/tbody/tr/td[6]/span/text()')
        currency_id = re.findall(r'https://coinmarketcap.com/currencies/(.*)/', response.url)[0]

        # 日志记录
        log_text = 'bitcoin_markets 没有抓取到数据 ' if (not currency_id) or (not market) else 'bitcoin_markets 数据已抓取'
        scrapy.log.msg(log_text, level=log.INFO if '数据已抓取' in log_text else log.ERROR)

        for i in range(0,len(unit)):
            if unit[i][-4:] in ['/USD','/CNY']:
                tradetime = int(round(time.time() * 1000))
                self.data = self.parase_str_list(currency_id, market[i], price[i], tradetime, volume_24h[i],valume_rate[i], unit[i])
                yield self.data

    def parase_str_list(self,currency_id,market,price,tradetime,volume_24h,valume_rate,unit):
        data = BitcoinMarketsItem()
        market_list = ['Livecoin',
        'Stellar Decentralized Exchange',
        'GDAX',
        'Ripple China',
        'Ore.Bz',
        'Neraex',
        'Bitstamp',
        'BitFlip',
        'BitKonan',
        'YoBit',
        'COSS',
        'xBTCe',
        'TOPBTC',
        'LakeBTC',
        'Omicrex',
        'RippleFox',
        'OkCoin Intl.',
        'Lykke Exchange',
        'Waves Decentralized Exchange',
        'Simex',
        'Coinsuper',
        'Exmo',
        'Fatbtc',
        'Exrates',
        'BitMEX',
        'Gatehub',
        'Mr. Exchange',
        'Abucoins',
        'Octaex',
        'C-CEX',
        'DSX',
        'Coinroom',
        'Bittylicious',
        'Bitfinex',
        'Kraken',
        'CoinsBank',
        'Bitstamp (Ripple Gateway)',
        'OKCoin.cn',
        'BTCC',
        'Sistemkoin',
        'WEX',
        'Bitsane',
        'Bitinka',
        'OEX',
        'BTC-Alpha',
        'Coinut',
        'BitBay',
        'Gemini',
        'Gatecoin',
        'SouthXchange',
        'Bitlish',
        'Coinhub',
        'CRXzone',
        'Quoine',
        'CEX.IO',
        'itBit',
        'Ethfinex'
        ]
        if market in market_list:
            data['market_id'] = market_list.index(market) + 1
            data['currency_id'] = currency_id
            data['price'] = 100
            data['tradetime'] = tradetime
            data['volume_24h'] = int(volume_24h)
            data['valume_rate'] = valume_rate
            if unit[-4:] == '/USD':
                data['unit'] = 1
            else:
                data['unit'] = 2
            print (data['currency_id'],data['market_id'],data['price'],data['tradetime'],data['volume_24h'],data['valume_rate'],data['unit'])
            print ('-------------------------')
            return data
