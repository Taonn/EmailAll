#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-04 07:15:27
LastEditors: zmf96
LastEditTime: 2022-03-04 07:38:53
FilePath: /emailall/config/__init__.py
Description: 
'''
import importlib

class Settings(object):
    def __init__(self):
        setting_modules = ['emailall.config.setting','emailall.config.api']
        for setting_module in setting_modules:
            print(setting_module)
            setting = importlib.import_module(setting_module)
            for attr in dir(setting):
                setattr(self, attr, getattr(setting,attr))
settings = Settings()