# -*- coding: utf-8 -*-
import sys
from email.header import Header
from email.mime.text import MIMEText
from scrapy.utils.project import get_project_settings
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy import signals
import smtplib


class EmailSender(object):

    def __init__(self,stats,spider_name):
        settings = get_project_settings()
        self.stats = stats
        self.spider_name = spider_name
        self.mail_host = settings.get('MAIL_HOST')      # 发送邮件的smtp服务器
        self.mail_user = settings.get('MAIL_USER')      # 发件人的用户名/邮箱账号
        self.mail_pass = settings.get('MAIL_PASS')      # 授权码
        self.smtp_port = 465            # smtp服务器SSL端口号，默认是465
        self.receivers = settings.get('MAIL_USER')      # 收件人邮箱账号
        print (self.mail_host)
        print (self.mail_user)
        print (self.mail_pass)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats,crawler.spider.name)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o ,#cls(o.stats),

    def spider_closed(self):
        ERROR1 = self.stats.get_value('log_count/ERROR')
        print (self.stats.get_stats())
        print ('ERROR1：'+ str(ERROR1))
        if ERROR1:
            self.sendEmail(ERROR1)

    def sendEmail(self,ERROR1):
        message = MIMEText('错误次数：' + str(ERROR1), 'plain', 'utf-8')  # 邮件内容
        subject = self.spider_name + ' 出错'
        message['Subject'] = Header(subject,'utf-8')  # 邮件主题
        message['From'] = self.mail_user  # 发件人名 Tim<lsz@guruhk.com>
        message['To'] = self.receivers  # 收件人名
        try:
            server = smtplib.SMTP_SSL(self.mail_host, 465)  # 发件人邮箱中的SMTP服务器，端口是465
            loginRes = server.login(self.mail_user, self.mail_pass)  # 登录smtp服务器,括号中对应的是发件人邮箱账号、邮箱密码

            if loginRes and loginRes[0] == 235:
                print (loginRes[0])             # loginRes = (235, b'Authentication successful')
                server.sendmail(self.mail_user, [self.receivers], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                print ("send_success")
            else:
                print ("Error: login_fail")
            server.quit()  # 关闭连接
        except smtplib.SMTPException:
            print("Error: send_fail")
        except Exception as e:
            print (e)

