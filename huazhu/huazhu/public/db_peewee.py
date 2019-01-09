# -*- coding: utf-8 -*-
import logging
from peewee import MySQLDatabase, Model, CharField, DateField, BooleanField, IntegerField,FloatField,BigIntegerField,DoubleField

# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

test_db = MySQLDatabase('spiderdb',host='218.244.138.88', user='spiderdb', passwd='Cqmyg321', charset='utf8', port=13456)
online_db = MySQLDatabase('spiderdb',host = '114.215.177.242', user='spiderdb', passwd='Cqmyg321', charset='utf8', port = 3306)



class BaseModel(Model):
    class Meta:
        database = test_db

class ipv4(BaseModel):
    apnic = CharField(verbose_name='apnic', max_length=10, null=True, index=True,default=None)
    en = CharField(verbose_name='en', max_length=20, null=True, default=None)
    ipv4 = CharField(verbose_name='ipv4', max_length=50, null=True, unique=True,default=None)
    ip = CharField(verbose_name='ip', null=True, default=None)
    num = IntegerField(verbose_name='num', null=True, default=None)
    public_timestamp = IntegerField(verbose_name='public_timestamp', null=True,default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class boc_exchange_rate(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    en_name = CharField(verbose_name='en_name', max_length=255, null=True, default=None)
    cn_name = CharField(verbose_name='cn_name', max_length=255, null=True, default=None)
    exchange_rate = FloatField(verbose_name='exchange_rate', null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class jinse(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    title = CharField(verbose_name='title', max_length=255, null=True, default=None)
    text = CharField(verbose_name='text', max_length=5000, null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class walian(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    title = CharField(verbose_name='title', max_length=255, null=True, default=None)
    text = CharField(verbose_name='text', max_length=5000, null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class walian_kuaixun(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    title = CharField(verbose_name='title', max_length=255, null=True, default=None)
    text = CharField(verbose_name='text', max_length=5000, null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class bishijie_kuaixun(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    title = CharField(verbose_name='title', max_length=255, null=True, default=None)
    text = CharField(verbose_name='text', max_length=5000, null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class t_bourse_quote(BaseModel):
    currency_id = CharField(verbose_name='currency_id',max_length=255,  null=True, index=True, default=None)
    market_id = IntegerField(verbose_name='market_id', null=True, default=None)
    tradetime = BigIntegerField(verbose_name='tradetime', null=True, default=None)
    price = DoubleField(verbose_name='price',null=True, default=None)
    market_cap_by_available_supply = BigIntegerField(verbose_name='market_cap_by_available_supply', null=True, default=None)
    volume_24h = BigIntegerField(verbose_name='volume_24h',  null=True, index=True,default=None)
    valume_rate = FloatField(verbose_name='valume_rate', null=True, default=None)
    unit = IntegerField(verbose_name='unit', null=True,default=None)
    record_timestamp = BigIntegerField(verbose_name='record_timestamp', null=True,default=None)
    standby1 = CharField(verbose_name='standby1', max_length=255, null=True, default=None)
    standby2 = CharField(verbose_name='standby2', max_length=255, null=True, default=None)

class t_coinmarketcap_daily_quote(BaseModel):
   currency_id = CharField(verbose_name='currency_id',max_length=255,  null=True, index=True, default=None)
   publish_timestamp = BigIntegerField(verbose_name='publish_timestamp', null=True, default=None)
   open_price = DoubleField(verbose_name='open_price',null=True, default=None)
   high_price = DoubleField(verbose_name='high_price',null=True, default=None)
   low_price = DoubleField(verbose_name='low_price',null=True, default=None)
   close_price = DoubleField(verbose_name='close_price',null=True, default=None)
   turnover_volume = BigIntegerField(verbose_name='turnover_volume', null=True, default=None)
   marke_value = BigIntegerField(verbose_name='marke_value', null=True, default=None)
   unit = CharField(verbose_name='unit',max_length=20,  null=True, index=True, default=None)
   update_time = BigIntegerField(verbose_name='update_time', null=True, default=None)
   standby1 = CharField(verbose_name='standby1', max_length=255, null=True, default=None)
   standby2 = CharField(verbose_name='standby2', max_length=255, null=True, default=None)

