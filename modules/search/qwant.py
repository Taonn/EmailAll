#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)

# !/usr/bin/python3
# -*- coding:utf-8 -*-
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
from common.search import Search
import time


class Qwant(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'QwantSearch'
        self.addr = 'https://api.qwant.com/v3/search/web'
        self.timeout = 2
        self.urls = list()
        self.limit_num = 300

    def search(self):
        self.per_page_num = 0
        while True:
            time.sleep(self.delay)
            query = '@' + self.domain
            params = {'q': query,
                      'count': 10,
                      'locale': 'zh_CN',
                      'offset': self.per_page_num,
                      'device': 'desktop',
                      'safesearch': 1
                      }
            resp = self.get(self.addr, params)
            if not resp:
                return
            data = resp.json()
            for urls in data['data']['result']['items']['mainline'][0]['items']:
                rep = self.get(urls['url'])
                emails = self.match_emails(rep)
                if emails:
                    self.results.update(emails)
                else:
                    continue
            self.page_num += 1
            if self.per_page_num == 0:
                self.per_page_num = 10
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
    search = Qwant(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
