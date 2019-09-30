#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from libs import tool
from libs import update

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 检查输入参数
if len(sys.argv) < 2:
    tool.log('缺少参数 mode(staging, release, push, back), os(ios, android)')
    quit()

# 操作模式
mode = sys.argv[1]

# 打包系统
os = ""
if len(sys.argv) > 2:
    os = sys.argv[2]


if mode == "staging":
    if os == "ios":
        update.update_ios_staging()
    elif os == "android":
        update.update_android_staging()
    else:
        update.update_ios_staging()
        update.update_android_staging()
    quit()

if mode == "release":
    if os == "ios":
        update.update_ios_release()
    elif os == "android":
        update.update_android_release()
    else:
        update.update_ios_release()
        update.update_android_release()
    quit()

if mode == "push":
    if os == "ios":
        update.update_ios_push()
    elif os == "android":
        update.update_android_push()
    else:
        update.update_ios_push()
        update.update_android_push()
    quit()

if mode == "back":
    if os == "ios":
        update.update_ios_back()
    elif os == "android":
        update.update_android_back()
    else:
        update.update_ios_back()
        update.update_android_back()
    quit()

tool.log("无效的 mode，请输入 staging/release/push/back")
