#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
from libs import tool

# 当前工作目录
workPath = os.getcwd()
print workPath

# json文件路径 react-native-upload
jsonPath = os.path.join(workPath, __file__, "libs/script.json")
print jsonPath
