#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import shutil
from libs import tool

# 当前工作目录
workPath = os.getcwd()
print workPath

# 创建 script.json 文件
json_in_path = os.path.join(sys.path[0], "libs/script.json")
json_out_path = os.path.join(workPath, "script.json")
print json_in_path
if os.path.isfile(json_out_path) is False:
    shutil.copy(json_in_path, workPath)
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

# 安装xcode解析库
