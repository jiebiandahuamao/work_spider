# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import time
import scrapy
import datetime
import MySQLdb


class PeriodicspidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WalianItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 文本
    text = scrapy.Field()
    #urllink
    page_link=scrapy.Field()
    # 入库时间戳
    record_timestamp = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into walian(page_link,title,text,record_timestamp) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE text=VALUES(text),title=VALUES(title)
        """
        record_timestamp = int(time.time())
        params = (self['page_link'],self['title'], self['text'], record_timestamp)
        return insert_sql, params


class WalianKuaixunItem(scrapy.Item):

    # 标题
    title = scrapy.Field()
    # 文本
    text = scrapy.Field()
    # 入库时间戳
    record_timestamp = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into walian_kuaixun(title,text,record_timestamp) values (%s,%s,%s) ON DUPLICATE KEY UPDATE text=VALUES(text)
        """
        record_timestamp = int(time.time())
        params = (self['title'], self['text'], record_timestamp)

        return insert_sql, params


class JinseItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 文本
    text = scrapy.Field()
    # urllink
    page_link = scrapy.Field()
    # 入库时间戳
    record_timestamp = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into jinse(page_link,title,text,record_timestamp) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE text=VALUES(text),title=VALUES(title)
        """
        record_timestamp = int(time.time())
        params = (self['page_link'],self['title'], self['text'], record_timestamp)

        return insert_sql, params


class BishijieKuaixunItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 文本
    text = scrapy.Field()
    # urllink
    page_link = scrapy.Field()
    # 入库时间戳
    record_timestamp = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into bishijie_kuaixun(page_link,title,text,record_timestamp) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE text=VALUES(text),title=VALUES(title)
        """
        record_timestamp = int(time.time())
        params = (self['page_link'],self['title'], self['text'], record_timestamp)
        return insert_sql, params


class HistoricalDataItem(scrapy.Item):

    # 币种id 例如（bitcoin）
    currency_id = scrapy.Field()
    # 日期时间戳（毫秒）
    publish_timestamp = scrapy.Field()
    # 开盘价
    open_price = scrapy.Field()
    # 最高价
    high_price = scrapy.Field()
    # 最低价
    low_price = scrapy.Field()
    # 收盘价
    close_price = scrapy.Field()
    #成交量
    turnover_volume = scrapy.Field()
    # 市值
    marke_value = scrapy.Field()
    # 配对单位（USD、CNY）
    unit = scrapy.Field()
    # 入库时间戳（毫秒）
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into t_coinmarketcap_daily_quote(currency_id,publish_timestamp,open_price,high_price,low_price,close_price,turnover_volume,marke_value,unit,update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE open_price=VALUES(open_price),high_price=VALUES(high_price),low_price=VALUES(low_price),close_price=VALUES(close_price),turnover_volume=VALUES(turnover_volume),marke_value=VALUES(marke_value),unit=VALUES(unit),update_time=VALUES(update_time)
        """
        record_timestamp = int(time.time())
        params = (self['currency_id'], self['publish_timestamp'],self['open_price'], self['high_price'], self['low_price'], self['close_price'], self['turnover_volume'], self['marke_value'], self['unit'], record_timestamp)

        return insert_sql, params


class BitcoinMarketsItem(scrapy.Item):

    # 币种id 例如（bitcoin）
    currency_id = scrapy.Field()
    #市场id
    market_id = scrapy.Field()
    # 现价
    price = scrapy.Field()
    # 交易时间戳（毫秒）
    tradetime = scrapy.Field()
    # 24小时成交量
    volume_24h = scrapy.Field()
    # 交易量百分比（已转百分数的小数）
    valume_rate = scrapy.Field()
    # 配对单位（1代表美元、2代表人民币）
    unit = scrapy.Field()
    # 入库时间戳（毫秒）
    record_timestamp = scrapy.Field()
    #'可流通市值'（暂未使用）
    market_cap_by_available_supply = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into t_bourse_quote(currency_id,market_id,price,tradetime,volume_24h,valume_rate,unit,record_timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE volume_24h=VALUES(volume_24h),price=VALUES(price),valume_rate=VALUES(valume_rate)
        """
        record_timestamp = int(time.time())
        params = (self['currency_id'],self['market_id'],self['price'],self['tradetime'],self['volume_24h'],self['valume_rate'],self['unit'],record_timestamp)

        return insert_sql, params


class BocExchangeRateItem(scrapy.Item):

    #代码，1000=USD 美元 ，1100=HKD 港元，1160=JPY 日元，1210=MOP 澳门元，1220=MYR 马来西亚林吉特，1320=SGD 新加坡元，1420=CNY 人民币，1430=TWD 台湾元，3000=EUR 欧元，3030=GBP 英镑，5010=CAD 加拿大元，6010=AUD 澳大利亚元
    code = scrapy.Field()
    #英文简称
    en_name = scrapy.Field()
    #中文名
    cn_name = scrapy.Field()
    #对比人民币汇率（1当前货币比上1人民币汇率）
    exchange_rate = scrapy.Field()
    #插入时间(精度天，单位秒)
    record_timestamp = scrapy.Field()
    def get_insert_sql(self):
        today_timestamp = int(time.mktime(datetime.date.today().timetuple()))
        db = MySQLdb.connect(host="218.244.138.88", port=13456, db="spiderdb", user="spiderdb", passwd="Cqmyg321",charset='utf8')
        cursor = db.cursor()
        sql = "select count(id) from boc_exchange_rate where record_timestamp>{};".format(today_timestamp)
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        if result[0] == 0:
            insert_sql = """
               insert into boc_exchange_rate(code,en_name,cn_name,exchange_rate,record_timestamp) values (%s,%s,%s,%s,%s)
               """
            record_timestamp = int(time.time())
            params = (self['code'], self['en_name'], self['cn_name'], self['exchange_rate'],record_timestamp)

            return insert_sql, params
        else:
            pass