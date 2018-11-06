# -*- coding: utf-8 -*-

import json
import redis
import MySQLdb


class DatabaseConnectionHandle:

	def __init__(self):
		online_db = {
				  "mysql":{
					  "host":"114.215.177.242",
					  "port":3306,
					  "user":"spiderdb",
					  "passwd":"Cqmyg321",
					  "db":"spiderdb",
					  "charset":"utf8"
						},
				   "redis":{
					   "host":"r-bp106663e776c6d4.redis.rds.aliyuncs.com",
					   "port":6379,
					   "db":0,
					"password":"Jtwmy43214"
					 }
				}

		test_db = {
			"mysql":{
				"host":"218.244.138.88",
				"port":13456,
				"user":"spiderdb",
				"passwd":"Cqmyg321",
				"db":"spiderdb",
				"charset":"utf8"
			},
			"redis":{
				"host":"218.244.138.88",
				"port":14555,
				"db":1,
				"password":""
			}
}

		config_json = test_db

		self.redis_config = config_json['redis']
		self.mysql_config = config_json['mysql']


	def get_cache_redis_connectin(self):
		r = redis.Redis(host=self.redis_config["host"],port=self.redis_config['port'],db=self.redis_config['db'],password=self.redis_config['password'])
		return r



	def get_spider_connection(self):
		conn = MySQLdb.connect(
			host = self.mysql_config['host'],
			port = self.mysql_config['port'],
			user = self.mysql_config['user'],
			passwd = self.mysql_config['passwd'],
			db = self.mysql_config['db'],
			charset = self.mysql_config['charset']
		)

		return conn