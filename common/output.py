#!/usr/bin/python3
# -*- coding:utf-8 -*- 
#
# @name   : EmailAll - Email Information Gathering Tools
# @url    : http://github.com/Taonn
# @author : Tao. (Taonn)
from prettytable import PrettyTable
from config import settings
import json


class Output(object):
    def __init__(self):
        self.emails = None

    def run(self, domain):
        """

        :param domain: 保存域名汇总成json文件的文件名
        :return:
        """
        pt = PrettyTable()
        path = settings.result_save_dir.joinpath(domain.replace('.', '_'))
        filename =domain + '_All' + '.json'
        path = path.joinpath(filename)
        with open(path, 'r', errors='ignore') as f:
            self.emails = json.load(f)
        pt.field_names = ['Index', 'Email']
        for i in range(self.emails['total']):
            d = list()
            d.append(i + 1)
            d.append(self.emails['emails'][i])
            pt.add_row(d)
        print(pt)