#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
import time
import base64

from common.search import Search
from config import settings
from config.log import logger
from common import utils


class Github(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Search'
        self.source = 'GithubApi'
        self.delay = 6
        self.addr = 'https://api.github.com/search/code'
        self.limit_num = 1000

    def match_emails(self, content):

        return utils.match_emails(self.domain, content)

    def search(self):
        try:

            self.page_num = 1
            self.per_page_num = 100

            while True:
                self.header.update({'Accept': 'application/vnd.github.v3.text-match+json',
                                    'Authorization': f"token {settings.github_token}"})
                time.sleep(self.delay)
                params = {'q': self.domain, 'per_page': self.per_page_num,
                          'page': self.page_num, 'sort': 'indexed',
                          'access_token': settings.github_token}

                resp = self.get(self.addr, params=params)
                items = resp.json()['items']
                if items:
                    urls = list()
                    for i in range(len(items)):
                        urls.append(items[i]['url'])
                    for url in urls:
                        rep = self.get(url.split('?')[0])
                        try:
                            if hasattr(rep, 'json'):
                                content = rep.json()['content']
                                content = base64.b64decode(content).decode()
                                emails = self.match_emails(content)
                                if emails:
                                    self.results.update(emails)
                                else:
                                    continue
                            else:
                                continue
                        except Exception as e:
                            logger.log('ALERT', e)
                            break
                self.page_num += 1

                if self.page_num * self.per_page_num >= self.limit_num:
                    break

        except Exception as e:
            logger.log('ALERT', e)

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
    search = Github(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
