#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
from common.search import Search
from urllib.parse import unquote,quote
from config import settings
import requests

import json


class Veryvp(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.domain = domain
        self.module = 'Datasets'
        self.source = 'Veryvp'
        self.addr = 'http://www.veryvp.com/SearchEmail/GetEmailList'
        self.num = 999

    def search(self):
        login_url = "http://veryvp.com/user/Login"
        login_par = {"UserName":settings.veryvp_username,
                     "Password":settings.veryvp_password,
                     "ValidateCode":"",
                     "KeepPassword":"0"}
        login_par = {
            'json': unquote(str(login_par)),
        }

        rep = self.post(login_url,login_par)
        if "登录成功" in rep.text:
            self.cookie = requests.utils.dict_from_cookiejar(rep.cookies)

            params = {'Key': self.domain,
                      'Order': '',
                      'PageSize': self.num,
                      'PageNo': 1}
            self.header.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            resp = self.post(url=self.addr, data=params)
            result = json.loads(resp.text)
            data = eval(result)
            data = data['Data']
            data = unquote(data)
            emails = list()

            if isinstance(data,str):
                for e in eval(data):
                    emails.append(e["email"])
                self.results.update(emails)
            else:
                pass
        else:
            pass

    def run(self):
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.save_res()


def run(domain):
    search = Veryvp(domain)
    search.run()


if __name__ == '__main__':
    run('example.com')
