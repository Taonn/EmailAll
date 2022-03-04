#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-04 07:15:27
LastEditors: zmf96
LastEditTime: 2022-03-04 08:05:37
FilePath: /emailall/modules/collect.py
Description: 
'''
#!/usr/bin/python3
# coding=utf-8
# Author: @Tao.

import threading
import importlib

from emailall.config.log import logger
from emailall.config import settings


class Collect(object):

    def __init__(self, domain):
        self.domain = domain
        self.modules = []
        self.collect_funcs = []

    def get_mod(self):
        """
        Get modules
        """
        # modules = ['certificates', 'check', 'datasets',
        #            'dnsquery', 'intelligence', 'search']
        modules = ['datasets','search']
        for module in modules:
            module_path = settings.modules_storage_dir.joinpath(module)
            for path in module_path.rglob('*.py'):
                import_module = f'emailall.modules.{module}.{path.stem}'
                self.modules.append(import_module)

    def import_func(self):
        """
        Import do function
        """
        for module in self.modules:
            name = module.split('.')[-1]
            import_object = importlib.import_module(module)
            func = getattr(import_object, 'run')
            self.collect_funcs.append([func, name])

    def run(self):
        """
            Class entrance
        """
        logger.log('INFOR', f'Start collecting Emails of {self.domain}')
        self.get_mod()
        self.import_func()

        threads = []

        for func_obj, func_name in self.collect_funcs:
            thread = threading.Thread(target=func_obj, name=func_name,
                                      args=(self.domain,), daemon=True)
            threads.append(thread)

        for t in threads:
            t.start()

        for t in threads:
            t.join(6*60)

        for t in threads:
            if t.is_alive():
                logger.log('ALERT', f'{t.name} module thread timed out')


if __name__ == '__main__':
    collect = Collect('example.com')
    collect.run()