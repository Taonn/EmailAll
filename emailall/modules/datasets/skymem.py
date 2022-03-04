#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)

from emailall.common.search import Search
import re


class Skymem(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Datasets'
        self.source = 'Skymem'
        self.addr = 'https://www.skymem.info'

    def search(self):
        # first 获取加密domain
        params = {'q': self.domain, 'ss': 'home'}
        resp = self.get(url=self.addr + '/srch', params=params)
        enc_domain = re.findall(r"Doc\.DomainEmails\.IdEntity='(.*?)'", resp.text)[0]
        if enc_domain:
            for i in range(1, 11):
                params = {'p': int(i)}
                rep = self.get(url=self.addr + '/domain/' + enc_domain, params=params)
                emails = self.match_emails(rep)
                if emails:
                    self.results.update(emails)
                else:
                    continue

    def run(self):
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.save_res()


def run(domain):
    search = Skymem(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
