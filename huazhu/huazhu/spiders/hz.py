# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import requests
from PIL import Image
from io import BytesIO
from huazhu.tools import pic_num

class HzSpider(scrapy.Spider):
    name = 'hz'
    allowed_domains = ['hotels.huazhu.com']
    # start_urls = ['http://hotels.huazhu.com/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'agency_middlewares.JavaScriptMiddleware': 500},
    }

    def start_requests(self):
        url = 'http://hotels.huazhu.com/?CityID=4403&CheckInDate=2018-11-16&CheckOutDate=2018-11-17'
        yield Request(url, callback=self.parse)

    def parse(self, response):
        pic_html = response.body
        pic_code = re.findall("\.p29_0_10\{background-image: url\(\\\\'\/Blur\/Pic\?b=(.*?)\\\\'\);",str(pic_html))
        jpg_link = 'http://hotels.huazhu.com/Blur/Pic?b={}'.format(pic_code[0])
        url_response = requests.get(jpg_link)
        image = Image.open(BytesIO(url_response.content))
        image.save('C:/Users/28674/Desktop/hz_pic_code/1.png')
        num = pic_num('C:/Users/28674/Desktop/hz_pic_code','1.png')
        price_var1 = response.xpath('//*[@id="Plist_hotel"]/div[3]/div/div/div/div[3]/div[1]/span/var[1]/@class')
        price_var2 = response.xpath('//*[@id="Plist_hotel"]/div[3]/div/div/div/div[3]/div[1]/span/var[2]/@class')
        price_var3 = response.xpath('//*[@id="Plist_hotel"]/div[3]/div/div/div/div[3]/div[1]/span/var[3]/@class')

        patton = 'p29_0_(\d+)'
        price = []
        for i in range(len(price_var1)):
            a = re.search(patton, str(price_var1[i]))
            b = re.search(patton, str(price_var2[i]))
            c = re.search(patton, str(price_var3[i]))
            price.append(str(num[int(a.group(1))])+str(num[int(b.group(1))])+str(num[int(c.group(1))]))

        name = response.xpath('//*[@id="Plist_hotel"]/div[3]/div/div/div/div[2]/div[1]/a/@title')
        address = response.xpath('//*[@id="Plist_hotel"]/div[3]/div/div/div/div[2]/div[2]/text()')

        next_url = None
