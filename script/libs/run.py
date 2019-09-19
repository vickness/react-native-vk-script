#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import json
import tool

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 当前工作目录
workPath = os.getcwd()

# 读取json文件
with open(os.path.join(workPath, "exports/script.json"), "r+") as f:
    data = json.load(f)
    # 当前版本号
    version = data["version"]
    # app渠道
    channel = data["channel"]
    # 包名渠道
    bundleId = data["appBundleID"]
