#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)


import time
from common.search import Search
from config.log import logger
from lxml import etree
from config import settings


class Ask(Search):

    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'AskSearch'
        self.addr = 'https://www.ask.com/web'
        self.urls = list()
        self.timeout = 15
        self.limit_num = 50
        self.per_page_num = 10

    def get_urls(self, html):
        html = etree.HTML(html)
        urls = html.xpath("//div[@class='PartialSearchResults-results']//a/@href")
        for url in urls:
            self.urls.append(url)

    def search(self):
        self.page_num = 1
        while True:
            time.sleep(self.delay)
            self.proxy = settings.proxy
            query = 'intext:@' + self.domain
            params = {'q': query, 'page': self.page_num}
            resp = self.get(self.addr, params=params)
            if not resp and not hasattr(resp, 'text'):
                logger.log('ERROR', f'For module {self.source}, you need to configure the proxy in setting.py file')
                break
            self.get_urls(resp.text)
            self.proxy = None
            for url in self.urls:
                rep = self.get(url)
                emails = self.match_emails(rep)
                if emails:
                    self.results.update(emails)
                else:
                    continue
            self.page_num += 1
            if '>Next<' not in resp.text:
                break

    def run(self):
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.save_res()

def run(domain):
    """
    类统一调用入口

    :param str domain: 域名
    """
    search = Ask(domain)
    search.run()

if __name__ == '__main__':
    run('example.com')
