# !/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import tool

# 当前工作目录
workPath = os.getcwd()
tool.log(workPath)

# icon图片尺寸
iosIconSize = ['20@2x', '20@3x', '29@2x', '29@3x', '40@2x', '40@3x', '60@2x', '60@3x', '1024@1x']
androidIconSize = [48, 72, 96, 144, 192]
androidNames = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']

# icon输出路径
iosIconOutPutPath = ""
androidIconOutPutPath = "./android/app/src/main/res/"

# icon输入路径
iconInputPath = ""

# 检查输入路径是否有效
if len(sys.argv) <= 1 or os.path.exists(sys.argv[1]) is False:
    tool.log('输入图片路径无效')
    quit()

# 遍历iOS工程路径，找到输出路径
for root, dirs, files in os.walk(workPath, topdown=False):
    for name in dirs:
        if name.endswith("Images.xcassets"):
            iosIconOutPutPath = os.path.join(root, name, "AppIcon.appiconset/")
            print(iosIconOutPutPath)

if len(iosIconOutPutPath) <= 0:
    tool.log('未找到Images.xcassets')
    quit()

# 遍历Android工程路径，找到输出路径
