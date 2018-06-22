
from scrapy import cmdline
import sys
import os

sys.path.append(os.path.abspath('../public'))

cmdline.execute("scrapy crawl bm_spider".split())
