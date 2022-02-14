#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)

from common.search import Search
from lxml import etree
from config import settings
from prettytable import PrettyTable


class EmailF(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Datasets'
        self.source = 'Email-Format'
        self.addr = f'https://www.email-format.com/d/{self.domain}/'
        self.resp = None
        self.ptf = PrettyTable(["Email_Rule", "Percent", "Example"])

    def search(self):
        self.resp = self.get(url=self.addr)
        emails = self.match_emails(self.resp)
        if emails:
            self.results.update(emails)
        else:
            pass

    def get_emails_rule(self):

        html = etree.HTML(self.resp.text)
        rule = html.xpath("//div[@class='format fl']/text()")
        pre = html.xpath("//div[@class='confidence_value fl']/text()")
        eg = html.xpath("//div[@class='format_example fl']/text()")
        for i in range(int(len(rule))):
            data = []
            data.append(rule[i].strip().replace('  ', '\033[7;31m+\033[0m').replace(' ', '\033[7;31m+\033[0m'))
            if i == 0:
                pre[i] = "\033[1;31m%s\033[0m" % pre[i]
            data.append(pre[i])
            data.append(eg[i])
            self.ptf.add_row(data)
        self.ptf.align["Email_Rule"] = 'l'
        self.ptf.align["Example"] = 'l'
        settings.rule_func.append(self.ptf)

    def run(self):
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.save_res()
        self.get_emails_rule()


def run(domain):
    search = EmailF(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
