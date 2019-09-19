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
    try:
        # 当前版本号
        version = data["version"]
        # app渠道
        channel = data["channel"]
        # 包名渠道
        bundleId = data["appBundleID"]
        # iOS热更新名称
        codePushIOS = data["codePushIOS"]
        # Android热更新名称
        codePushAndroid = data["codePushAndroid"]
    except KeyError, error:
        tool.log("未找到 exports/script.json 文件的 %s" % error)
        exit()

# 检测版本号
if len(version) <= 0:
    tool.log("未找到版本号，请检查 exports/script.json 文件 version 的值")
    exit()


def update_ios_staging():
    tool.log("开始更新 iOS Staging，版本号为：" + version)
    command = "code-push release-react %s ios -t %s" % (codePushIOS, version)
    tool.log("执行：" + command)
    code = os.system(command)
    if code == 0:
        tool.log("iOS 更新完成")
    else:
        tool.log("iOS 更新失败")
        exit()


def update_android_staging():
    tool.log("开始更新 Android Staging，版本号为：" + version)
    command = "code-push release-react %s android -t %s" % (codePushAndroid, version)
    tool.log("执行：" + command)
    code = os.system(command)
    if code == 0:
        tool.log("Android 更新完成")
    else:
        tool.log("Android 更新失败")
        exit()


def update_ios_release():
    input_str = raw_input("确定发布 iOS 更新(y/n)?")
    print input_str
    if input_str == "y":
        command = "code-push promote %s Staging Production" % codePushIOS
        tool.log("执行：" + command)
        code = os.system(command)
        if code == 0:
            tool.log("iOS 发布完成")
        else:
            tool.log("iOS 发布失败")
            exit()
    else:
        tool.log("输入错误，取消发布")
        exit()


def update_android_release():
    input_str = raw_input("确定发布 Android 更新(y/n)?")
    if input_str == "y":
        command = "code-push promote %s Staging Production" % codePushAndroid
        tool.log("执行：" + command)
        code = os.system(command)
        if code == 0:
            tool.log("Android 发布完成")
        else:
            tool.log("Android 发布失败")
            exit()
    else:
        tool.log("输入错误，取消发布")
        exit()
