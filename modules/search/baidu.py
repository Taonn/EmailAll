#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)


import time
from common.search import Search
from config.setting import emails
from lxml import etree


class Baidu(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'BaiduSearch'
        self.addr = 'https://www.baidu.com/s'
        self.urls = list()
        self.limit_num = 500
        self.per_page_num = 10

    def get_url(self, html):
        data = []
        html = etree.HTML(html)
        urls = html.xpath("//div[@id='content_left']//h3/a/@href")
        for url in urls:
            locat_url = self.match_location(url)
            time.sleep(2)
            data.append(locat_url)
            self.urls.append(locat_url)
        return data

    def search(self):
        while True:
            time.sleep(self.delay)
            query = 'intext:@' + self.domain
            params = {'wd': query,
                      'pn': self.page_num,
                      'rn': self.per_page_num}
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
            self.page_num += self.per_page_num
            if f'&amp;pn={self.page_num}&' not in resp.text:
                break
            if self.page_num >= self.limit_num:  # 搜索条数限制
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
    search = Baidu(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
