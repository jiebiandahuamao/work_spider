# -*- coding: utf-8 -*-
from scrapy import cmdline




cmdline.execute("scrapy crawl add_read -a url=http://www.sohu.com/a/239178870_162818 -a time=28000".split())