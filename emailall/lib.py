#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-04 04:58:33
LastEditors: zmf96
LastEditTime: 2022-03-04 10:01:37
FilePath: /emailall/lib.py
Description: 
'''
from emailall.modules.collect import Collect
from emailall.config import settings


def run_emailall(domain):
    col = Collect(domain)
    col.run()
    emails = set()
    for datas in settings.emails:
        for data in datas:
            emails.update(data['emails'])

    return emails


if __name__ == "__main__":
    print(run_emailall('example.com'))
