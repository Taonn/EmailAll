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


class Bingcn(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'BingcnSearch'
        self.addr = 'https://cn.bing.com/'
        self.urls = list()
        self.limit_num = 250

    def get_url(self, html):
        data = []
        html = etree.HTML(html)
        urls = html.xpath('//a[@class="sh_favicon"]/@href')
        for url in urls:
            data.append(url)
            self.urls.append(url)
        return data

    def search(self):
        self.page_num = 0  # 二次搜索
        resp = self.get(self.addr)
        if not resp:
            return
        self.cookie = resp.cookies
        while True:
            time.sleep(self.delay)
            query = 'intext:@' + self.domain
            params = {'q': query, 'first': self.page_num,
                      'count': self.per_page_num}
            resp = self.get(self.addr + '/search', params)
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
            if '<div class="sw_next">' not in resp.text:
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
    search = Bingcn(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
