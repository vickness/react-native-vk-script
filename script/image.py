#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
from libs import tool
from libs import icon
from libs import launch

# 检查输入路径
if len(sys.argv) <= 1:
    tool.log('缺少参数 option(icon, launch), path')
    quit()

if len(sys.argv) <= 2:
    tool.log('缺少参数 path')
    quit()

# 操作命令
option = sys.argv[1]

# 文件路径
path = sys.argv[2]

if option == "icon":
    icon_path = icon.check_icon_path(path)
    icon.create_ios_icon(icon_path)
    icon.create_android_icon(icon_path)
    quit()

if option == "launch":
    launch.check_splash_path(path)
    launch.create_ios_splash(path)
    launch.create_android_splash(path)
    quit()
