# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy','crawl','walian'])
execute(['scrapy','crawl','walian_kuaixun'])
execute(['scrapy','crawl','jinse'])
execute(['scrapy','crawl','bishijie_kuaixun'])
execute(['scrapy','crawl','historical_data'])
execute(['scrapy','crawl','bitcoin_markets'])
execute(['scrapy','crawl','boc_exchange_rate'])