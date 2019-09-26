#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import shutil
from libs import tool

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 当前工作目录
workPath = os.getcwd()

# 配置文件目录
exports_path = os.path.join(workPath, "exports")

# 创建 exports 文件夹
if not os.path.exists(exports_path):
    os.makedirs(exports_path)
    tool.log("创建 exports 目录")

app_path = os.path.join(exports_path, "apps")
if not os.path.exists(app_path):
    os.makedirs(app_path)

option_path = os.path.join(exports_path, "options")
if not os.path.exists(option_path):
    os.makedirs(option_path)

# 创建 script.json 文件
json_in_path = os.path.join(sys.path[0], "libs/script.json")
json_out_path = os.path.join(exports_path, "script.json")
if os.path.isfile(json_out_path) is False:
    shutil.copy(json_in_path, exports_path)
    tool.log("创建 script.json 文件")

# 安装图片处理库
try:
    from PIL import Image, ImageDraw
except ImportError:
    tool.log('缺少Image模块，正在安装Image模块，请等待...')
    success = os.system('python -m pip install Image')
    if success == 0:
        tool.log('Image模块安装成功.')
    else:
        tool.log('Image安装失败，请手动在终端执行：\'python -m pip install Image\'重新安装.')
        quit()

tool.log("初始化完成")
