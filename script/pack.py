#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from libs import tool
from libs import package

# 检查输入参数
if len(sys.argv) < 2:
    tool.log('缺少参数 mode(debug, staging, release), os(ios, android)')
    quit()

# 打包模式
mode = sys.argv[1]

# 打包系统
os = ""
if len(sys.argv) > 2:
    os = sys.argv[2]

if mode == "debug":
    if os == "ios":
        package.pack_ios_debug()
    elif os == "android":
        package.pack_android_debug()
    else:
        package.pack_ios_debug()
        package.pack_android_debug()
    quit()

if mode == "staging":
    if os == "ios":
        package.pack_ios_staging()
    elif os == "android":
        package.pack_android_staging()
    else:
        package.pack_ios_staging()
        package.pack_android_staging()
    quit()

if mode == "release":
    if os == "ios":
        package.pack_ios_release()
    elif os == "android":
        package.pack_android_release()
    else:
        package.pack_ios_release()
        package.pack_android_release()
    quit()

tool.log("无效的 mode，请输入 debug/staging/release")
