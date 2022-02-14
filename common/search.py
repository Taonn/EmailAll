#!/usr/bin/python3
# coding=utf-8
# Author: @Tao.

from modules.module import Module
from config import settings
from config.log import logger

import json


class Search(Module):

    def __init__(self):
        Module.__init__(self)
        self.page_num = 0  # 要显示搜索起始条数
        self.per_page_num = 50
        self.emails = list()

    def match_location(self, url):
        """

        :param url: 未location的url
        :return: 真实url
        """
        resp = self.head(url=url, check=False, allow_redirects=False)
        if not resp:
            return set()
        location = resp.headers.get('location')
        if not location:
            return set()
        return location

    def save_json(self):
        """
        保存每个modules的数据至json文件
        :return:
        """
        logger.log('TRACE', f'Save the Email results found by '
                            f'{self.source} module as a json file')
        path = settings.result_save_dir.joinpath(self.domain.replace('.', '_'))
        path.mkdir(parents=True, exist_ok=True)
        filename = self.source + '.json'
        path = path.joinpath(filename)

        results = {'name': self.module,
                   'source': self.source,
                   'total': len(self.results),
                   'emails': list(self.results)}

        with open(path, 'w', errors='ignore') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        self.emails.append(results)

    def save_res(self):
        """
        存储数据至全局变量，由于后面输出打印&存储汇总
        :return:
        """
        settings.emails.append(self.emails)