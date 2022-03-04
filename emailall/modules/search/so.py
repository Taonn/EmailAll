#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)

import time
from emailall.common.search import Search
from emailall.config.log import logger
from lxml import etree
import re


class So(Search):

    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'SoSearch'
        self.addr = 'https://www.so.com/s'
        self.urls = list()
        self.limit_num = 200
        self.delay = 4
        self.per_page_num = 10

    def match_location(self, url):
        try:
            if 'so.com/link' in url:
                resp = self.get(url=url)
                if not resp:
                    return
                location = re.findall(r'window\.location\.replace\("(.*?)"\)', resp.text)[0]
                if not location:
                    return
                return location
            else:
                return url
        except Exception as e:
            logger.log('ERROR', e)
            return

    def get_url(self, html):
        data = []
        html = etree.HTML(html)
        urls = html.xpath("//li[@class='res-list']//a[@rel='noopener']/@href")
        for url in urls:
            locat_url = self.match_location(url)
            time.sleep(1)
            if locat_url:
                data.append(locat_url)
                self.urls.append(locat_url)
        return data

    def search(self):
        self.page_num = 1
        while True:
            time.sleep(self.delay)
            query = '@' + self.domain
            params = {'q': query, 'pn': self.page_num}
            resp = self.get(self.addr, params)
            if not resp:
                return
            data = self.get_url(resp.text)
            for url in data:
                rep = self.get(url)
                emails = self.match_emails(rep)
                if emails:
                    self.results.update(emails)
                else:
                    continue
            self.page_num += 1
            if '<a id="snext"' not in resp.text:
                break
                # 搜索条数限制
            if self.page_num * self.per_page_num >= self.limit_num:
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
    search = So(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
