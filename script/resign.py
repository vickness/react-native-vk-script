#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
from libs import tool

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 当前工作目录
workPath = os.getcwd()

# 证书p12路径
p12_path = os.path.join(workPath, "exports/sign/resign.p12")
if not os.path.isfile(p12_path):
    tool.log("缺少文件：exports/sign/resign.p12")
    quit()

# 证书密码
p12_pwd = sys.argv[1]
if len(p12_pwd) <= 0:
    p12_pwd = ""

# profile路径
profile_path = os.path.join(workPath, "exports/sign/resign.mobileprovision")
if not os.path.isfile(profile_path):
    tool.log("缺少文件：exports/sign/resign.mobileprovision")
    quit()

# 生成的app路径
apps_path = os.path.join(workPath, "exports/apps")

# 查找.ipa文件
for root, dirs, files in os.walk(apps_path, topdown=False):
    for name in files:
        if name.endswith(".ipa") and not name.startswith("re_"):
            app_in_path = os.path.join(root, name)
            # print(app_in_path)
            app_out_path = os.path.join(root, "re_"+name)
            # print(app_out_path)
            # 重签名
            command = '%s/resign -k %s -p %s -m %s -o %s -z 9 %s' % (sys.path[0], p12_path, p12_pwd, profile_path, app_out_path, app_in_path)
            # tool.log(command)
            os.system(command)

    tool.log("重签名完成")
