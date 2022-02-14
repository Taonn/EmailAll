#!/usr/bin/python3
# coding=utf-8
# Author: @Tao.

import pathlib

"""
配置文件
"""
# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # EmailAll代码相对路径
modules_storage_dir = relative_directory.joinpath('modules')  # modules存放目录
result_save_dir = relative_directory.joinpath('result')

rule_func = list()

emails = list()
proxy = {'http': '127.0.0.1:2333', 'https': '127.0.0.1:2333'}
