# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os


# 输出函数
def log(text):
    print '\033[31m' + text + '\033[0m'


# 检查文件是否存在
def file_exist(path, func):
    _path = None
    # 获取所有文件遍历
    files = os.listdir(path)
    for name in files:
        each_path = os.path.join(path, name)
        exist = func(path, each_path)
        if exist:
            _path = each_path

    # 返回地址
    return _path
