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
import re


class Sogou(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'SogouSearch'
        self.addr = 'https://www.sogou.com/web'
        self.urls = list()
        self.limit_num = 200
        self.per_page_num = 10

    def match_location(self, url):
        try:
            if '/link?url=' not in url:
                return url
            else:
                resp = self.get(url=url)
                if not resp:
                    return set()
                location = re.findall(r'window\.location\.replace\("(.*?)"\)', resp.text)[0]
            if not location:
                return set()
            return location
        except Exception as e:
            logger.log('ERROR', e)

    def get_url(self, html):
        data = []
        html = etree.HTML(html)
        urls = html.xpath("//a[@name='dttl']/@href")
        base_url = self.addr.replace('/web', '')
        for url in urls:
            locat_url = self.match_location(base_url + url)
            time.sleep(2)
            data.append(locat_url)
            self.urls.append(locat_url)
        return data

    def search(self):
        self.page_num = 1
        while True:
            time.sleep(self.delay)
            query = 'intext:@' + self.domain
            params = {'query': query, 'page': self.page_num,
                      "num": self.per_page_num}
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
            if '<a id="sogou_next"' not in resp.text:
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
    search = Sogou(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
