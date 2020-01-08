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

# 库的目录
lib_path = sys.path[0]

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

sign_path = os.path.join(exports_path, "sign")
if not os.path.exists(sign_path):
    os.makedirs(sign_path)

# 创建 script.json 文件
json_in_path = os.path.join(lib_path, "libs/script.json")
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

# # 安装重签名工具
# tool.log('安装重签名工具')
# os.system('brew install openssl')
# os.system('brew upgrade openssl')
#
# zsign_path = "%s/zsign" % lib_path
# if os.path.isdir(zsign_path):
#     # tool.log('删除路径: %s' % zsign_path)
#     shutil.rmtree(zsign_path)
#
# os.system("cd %s && git clone https://github.com/zhlynn/zsign.git" % lib_path)
# os.system('cd %s && g++ *.cpp common/*.cpp -lcrypto -I/usr/local/Cellar/openssl/1.0.2t/include -L/usr/local/Cellar/openssl/1.0.2t/lib -O3 -o resign' % zsign_path)
#
# resign_file_path = "%s/resign" % zsign_path
# if not os.path.isfile(resign_file_path):
#     shutil.rmtree(zsign_path)
#     tool.log('安装失败')
#     quit()
#
# shutil.copy(resign_file_path, lib_path)
# shutil.rmtree(zsign_path)

tool.log("初始化完成")
