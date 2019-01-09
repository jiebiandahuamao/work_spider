# -*- coding: utf-8 -*-
import random
import socket
import urllib.request
import urllib.error
# import urllib2

from time import sleep
import re
import requests
import selenium
from scrapy.contrib.closespider import CloseSpider
from selenium.common.exceptions import TimeoutException
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium import webdriver
import scrapy
from scrapy import log
from scrapy.utils.project import get_project_settings


class JavaScriptMiddleware(object):

    def __init__(self,crawler):
        # 初始化代理超时计数
        self.timeout_time = 0
        # crawler.set('ENABLE_PROXY',11111)
        # a = crawler.get('ENABLE_PROXY')
        # print a
        settings = get_project_settings()
        self.GET_PROXY_URL = settings.get('GET_PROXY_URL')
        self.ENABLE_PROXY = settings.get('ENABLE_PROXY')
        print (self.ENABLE_PROXY)
        self.create_ua_proxy()
        print("starting...")


    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            sleep(random.uniform(1.9, 2))
            content = self.driver.page_source.encode('utf-8')
            # self.driver.refresh()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

        except TimeoutException or socket.error or selenium.common.exceptions.WebDriverException as e:
            # print e,e.msg
            scrapy.log.msg(e, e.msg, level=log.WARNING)
            self.timeout_counter()
        except urllib.error.URLError as e:
            scrapy.log.msg(Exception.__class__,e, level=log.WARNING)
        except Exception as e:
            print (e.__class__)
            print (repr(e))
            print (e,)
            scrapy.log.msg(repr(e), e, level=log.WARNING)

        return HtmlResponse(request.url, encoding='utf-8', request=request)
        # return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    # 生成随机代理和UA
    def create_ua_proxy(self):
        # UA列表
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",#OK
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Opera/9.80 (Windows NT 6.1; U; en)Presto/2.8.131 Version/11.11",
            # "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",手机界面
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",#OK
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",#okk
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",#ok
        ]

        # 使用代理

        if self.ENABLE_PROXY:
            self.proxy_list = []
            while len(self.proxy_list) == 0:
                self.get_proxy_url = self.GET_PROXY_URL
                self.proxy = urllib.request.urlopen(self.get_proxy_url)
                for line in self.proxy:
                    print (type(line))
                    if '"code":"3006"' in str(line):
                        scrapy.log.msg("'提取数量已用完'", level=log.WARNING)
                        raise Exception('提取数量已用完')
                    elif '"code":"3003"' in str(line):
                        scrapy.log.msg("'提取失败，请重试'", level=log.WARNING)
                        raise Exception('提取失败，请重试')
                    elif '"code":"3004"' in str(line):
                        scrapy.log.msg("'查不到订单，请输入正确的appKey'", level=log.WARNING)
                        raise Exception('查不到订单，请输入正确的appKey')
                    elif '"code":"3005"' in str(line):
                        scrapy.log.msg("'订单已过期!'", level=log.WARNING)
                        raise Exception('订单已过期!')
                    elif '"code":"3010"' in str(line):
                        scrapy.log.msg("'订单异常被冻结'", level=log.WARNING)
                        raise Exception('订单异常被冻结')
                    elif '"code":"3001"' in str(line):
                        scrapy.log.msg("'提取频繁，请重试'", level=log.WARNING)
                        sleep(random.uniform(5, 10))
                    elif '"ERRORCODE":"10032"' in str(line):
                        scrapy.log.msg("'今日提取已达上限，请隔日提取或额外购买'", level=log.WARNING)
                        raise Exception('今日提取已达上限，请隔日提取或额外购买')
                    elif '"ERRORCODE":"10055"' in str(line):
                        scrapy.log.msg("'提取过快，请至少5秒提取一次'", level=log.WARNING)
                        sleep(random.uniform(20, 25))
                    elif '"ERRORCODE":"10074"' in str(line):
                        scrapy.log.msg( "'代理IP已用完'", level=log.WARNING)
                        raise Exception('代理IP已用完')
                    else:
                        # line = re.search('{"(code|ERRORCODE)":"0","(msg|RESULT)":\[{"port":"(.*?)","ip":"(.*?)"}]}',line)
                        # print line.group(3),line.group(4)
                        # line = line.group(4) + ':' + line.group(3)
                        # print "proxy :" + line
                        # scrapy.log.msg( "proxy :" + line, level=log.WARNING)
                        self.proxy_list.append(line)


            # PhantomJS
            # self.dcap = dict(DesiredCapabilities.PHANTOMJS)
            # self.dcap["phantomjs.page.settings.userAgent"] = random.choice(USER_AGENTS)
            #
            # # 不载入图片，爬页面速度会快很多
            # self.dcap["phantomjs.page.settings.loadImages"] = False
            # self.service_args = [
            #     '--proxy=' + random.choice(self.proxy_list),
            #     '--proxy-type=http'
            # ]
            # self.service_args.append('--load-images=no')  ##关闭图片加载
            # self.service_args.append('--disk-cache=yes')  ##开启缓存
            # self.service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
            # scrapy.log.msg("proxy :" + str(random.choice(self.proxy_list)), level=log.WARNING)
            # scrapy.log.msg("UA :" + self.dcap["phantomjs.page.settings.userAgent"], level=log.WARNING)
            # self.driver = webdriver.PhantomJS(service_args=self.service_args,desired_capabilities=self.dcap)

            # Chrome
            options = webdriver.ChromeOptions()

            # 设置为headless模式 （必须）
            options.add_argument("--headless")
            # 图片不显示
            prefs = {
            'profile.default_content_setting_values': {
            'images': 2
            }
            }
            options.add_experimental_option('prefs', prefs)
            # # # 代理
            PROXY = random.choice(self.proxy_list)
            # # # UA
            options.add_argument('no-sandbox')
            options.add_argument('--lang=zh-CN,zh;q=0.9N')
            UA = random.choice(USER_AGENTS)
            options.add_argument('--user-agent=' + UA)
            # print PROXY,UA
            # DNS缓存
            # options.add_argument('--dns-prefetch-disable')
            # options.add_argument('--disk-cache=yes')#无效
            options.add_argument('--proxy-server=http://' + str(PROXY))
            self.driver = webdriver.Chrome(chrome_options=options)
        # 不使用代理
        elif not self.ENABLE_PROXY:
            # PhantomJS
            # self.driver = webdriver.PhantomJS()

            # Chrome
            options = webdriver.ChromeOptions()
            # 设置为headless模式 （必须）
            options.add_argument('no-sandbox')
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=options)

            # 窗口最大化和1440X900
            # options.add_argument("start-maximized")
            # self.driver.set_window_size(1440, 900)
            # newwindow = 'window.open("http://mp.cnfol.com/article/1218502");'
            # self.driver.execute_script(newwindow)

        # 设置5秒页面超时返回，类似于requests.get()的timeout选项，不设置程序会卡住
        self.driver.set_page_load_timeout(50)

    # 记录和重置错误计数器
    def timeout_counter(self):
        if self.ENABLE_PROXY:
            self.timeout_time += 1
            scrapy.log.msg('proxy--timeout：' + str(self.timeout_time), level=log.WARNING)
            if self.timeout_time < 2:
                pass
            elif self.timeout_time < 5:
                self.check_proxy()
            else:
                scrapy.log.msg('update_proxy:time_over', level=log.WARNING)
                self.timeout_time = 0
                self.driver.quit()
                self.create_ua_proxy()
        else:
            self.driver.quit()
            self.create_ua_proxy()

    def check_proxy(self):
        if not self.proxy_list == []:
            print (self.proxy_list[0])
            proxy_str = re.sub(':', '%3A', self.proxy_list[0])
            try:
                check_result = requests.get("http://www.xdaili.cn/ipagent//checkIp/ipList?ip_ports%5B%5D=" + proxy_str, timeout=15)
                print (check_result.content)
                delay = re.findall('"time":"(.*?)ms",', check_result.content)
                if delay:
                    # if int(delay[0]) < 1000 :
                    scrapy.log.msg('proxy_delay' + delay[0] + 'ms', level=log.WARNING)
                    # else:
                    #     print delay[0] + 'ms'
                    #     scrapy.log.msg( delay[0] + 'ms', level=log.WARNING)
                    #     print 'update_proxy:timeout' + delay[0] + 'ms'
                    #     self.timeout_time = 0
                    #     self.driver.quit()
                    #     self.create_ua_proxy()
                else:
                    scrapy.log.msg('update_proxy:timeout', level=log.WARNING)
                    self.timeout_time = 0
                    self.driver.quit()
                    self.create_ua_proxy()

            except Exception as e:
                print(e)
                self.timeout_time += 1
                scrapy.log.msg('proxy--timeout：' + str(self.timeout_time), level=log.WARNING)

    # 信号绑定
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.timeout_counter, signal=signals.spider_error)
        return o

    # 结束phantomJS进程
    def spider_closed(self):
        print ("spider_closed")
        # print self.driver.current_window_handle
        # print self.driver.window_handles
        # self.driver.save_screenshot('moount.png')
        self.driver.quit()








