#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
from common.search import Search
from config import settings
from config.log import logger


class PhoneBook(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Datasets'
        self.source = 'PhoneBook'
        self.addr = 'https://public.intelx.io/phonebook/search'
        self.num = 999
        self.key = settings.pb_key if settings.pb_key else "077424c6-7a26-410e-9269-c9ac546886a4"

    def search(self):

        self.header.update({'Referer': 'https://phonebook.cz/',
                            'Origin': 'https://phonebook.cz',
                            'sec-ch-ua-platform': '"Windows"',
                            'Sec-Fetch-Site': 'cross-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                            'Accept': '* / *',
                            'Content-Type': 'application / json',
                            })
        params = {"term": self.domain,
                  "maxresults": 10000,
                  "media": 0,
                  "target": 2,
                  "timeout": 20}
        url = self.addr + f'?k={self.key}'
        resp = self.post(url, json=params)
        if not resp:
            return
        if hasattr(resp, 'json'):
            id = resp.json()["id"]
            if not id:
                logger.log('ALERT', f'Get PhoneBook id fail')
                return
            params = {
                "k": self.key,
                "id": id,
                "limit": 10000
            }
            self.header.update({'TE': 'trailers'})
            rep = self.get(self.addr + '/result', params=params)
            if hasattr(rep, 'json'):
                emails = self.match_emails(rep)
                if emails:
                    self.results.update(emails)
                else:
                    pass

    def run(self):
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.save_res()


def run(domain):
    search = PhoneBook(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
