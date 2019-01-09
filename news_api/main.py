# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.abspath('../public'))

execute(['scrapy','crawl','get_news_api'])