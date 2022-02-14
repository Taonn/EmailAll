#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
from common.search import Search
import time
import re
from urllib.parse import unquote
from config.log import logger
from config import settings


class Google(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'GoogleSearch'
        self.addr = 'https://www.google.com/search'
        self.timeout = 10
        self.urls = list()

    def get_url(self, html):
        data = []
        urls = re.findall(r'href="/url\?q=(.*?)&amp;', html)
        for url in urls:
            url = unquote(url)
            data.append(url)
            self.urls.append(url)
        return data

    def search(self):
        page_num = 1
        per_page_num = 25
        self.header.update({'Referer': 'https://www.google.com'})
        self.proxy = settings.proxy
        resp = self.get(self.addr.replace('/search', ''))
        if not resp:
            logger.log('ERROR', f'For module {self.source}, you need to configure the proxy in setting.py file')
            return
        self.cookie = resp.cookies
        while True:
            time.sleep(self.delay)
            self.proxy = settings.proxy
            query = 'intext:@' + self.domain
            params = {'q': query, 'start': page_num, 'num': per_page_num,
                      'filter': '0', 'btnG': 'Search', 'gbv': '1', 'hl': 'en'}
            resp = self.get(self.addr, params)
            if not resp:
                return
            data = self.get_url(resp.text)
            for url in data:
                self.proxy = None
                if "google.com" not in url:
                    rep = self.get(url)
                    emails = self.match_emails(rep)
                    if emails:
                        self.results.update(emails)
                    else:
                        continue
                else:
                    pass
            page_num += per_page_num
            if 'start=' + str(page_num) not in resp.text:
                break
            if '302 Moved' in resp.text:
                break
            if page_num == 20:
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
    search = Google(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
