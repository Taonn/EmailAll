#!/usr/bin/python3
# coding=utf-8
# Author: @Tao.

import threading
import time
import requests
import urllib3

from config.log import logger
from prettytable import PrettyTable
from fake_useragent import UserAgent
from common import utils

urllib3.disable_warnings()

lock = threading.Lock()
ua = UserAgent()
ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
request_default_headers = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Referer': 'https://www.google.com/',
    'User-Agent': ua.random,
    'Upgrade-Insecure-Requests': '1',
    'X-Forwarded-For': ip
}
emails = set()


class Module(object):
    def __init__(self):
        self.module = 'Module'
        self.source = 'BaseModule'
        self.cookie = None
        self.header = request_default_headers
        self.proxy = None
        self.timeout = 5
        self.delay = 2
        self.verify = False
        self.domain = str()
        self.results = set()
        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时
        self.pt = PrettyTable()
        self.pt.field_names = ['Email', 'Source']

    def begin(self):
        """
        begin log
        """
        logger.log('INFOR', f'Start {self.source} module to '
                            f'collect Emaile of {self.domain}')

    def finish(self):
        """
              finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('DEBUG', f'Finished {self.source} module to '
                            f'collect {self.domain}\'s Email')
        logger.log('INFOR', f'{self.source} module took {self.elapse} seconds '
                            f'found {len(self.results)} Email')

    def get(self, url, params=None, check=True, ignore=False, raise_error=False, **kwargs):
        """
        Custom get request

        :param str  url: request url
        :param dict params: request parameters
        :param bool check: check response
        :param bool ignore: ignore error
        :param bool raise_error: raise error or not
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        level = 'ERROR'
        if ignore:
            level = 'DEBUG'
        try:
            resp = session.get(url,
                               params=params,
                               cookies=self.cookie,
                               headers=self.header,
                               proxies=self.proxy,
                               timeout=self.timeout,
                               verify=self.verify,
                               **kwargs)
        except Exception as e:
            if raise_error:
                if isinstance(e, requests.exceptions.ConnectTimeout):
                    logger.log(level, e.args[0])
                    raise e
            logger.log(level, e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('GET', resp):
            return resp
        return None

    def post(self, url, data=None, check=True, **kwargs):
        """
        Custom post request

        :param str  url: request url
        :param dict data: request data
        :param bool check: check response
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        try:
            resp = session.post(url,
                                data=data,
                                cookies=self.cookie,
                                headers=self.header,
                                proxies=self.proxy,
                                timeout=self.timeout,
                                verify=self.verify,
                                **kwargs)
        except Exception as e:
            logger.log('ERROR', e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('POST', resp):
            return resp
        return None

    def match_emails(self, resp):
        if not resp:
            return set()
        elif hasattr(resp, 'text'):
            return utils.match_emails(self.domain, resp.text)
        else:
            return set()

    def head(self, url, params=None, check=True, **kwargs):
        """
        Custom head request

        :param str  url: request url
        :param dict params: request parameters
        :param bool check: check response
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        try:
            resp = session.head(url,
                                params=params,
                                cookies=self.cookie,
                                headers=self.header,
                                proxies=self.proxy,
                                timeout=self.timeout,
                                verify=self.verify,
                                **kwargs)
        except Exception as e:
            logger.log('ERROR', e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('HEAD', resp):
            return resp
        return None
