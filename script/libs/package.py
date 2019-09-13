#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import tool

# 当前工作目录
workPath = os.getcwd()

# iOS项目路径
iosPath = os.path.join(workPath, "ios")

# iOS app 输出路径
export_ipa_path = os.path.join(iosPath, "build/apps")

# iOS app 编译路径
archive_path = os.path.join(iosPath, "build/xcarchive")

# 查询ios项目名称
ios_project_name = ""
for root, dirs, files in os.walk(iosPath, topdown=False):
    for name in dirs:
        if name.endswith("xcodeproj"):
            ios_project_name = name


def pack_android_debug():
    tool.log("Android Debug 开始打包...")
    os.system("cd android && ./gradlew clean")
    os.system("cd android && ./gradlew assembleDebug")
    tool.log("Android Debug 打包结束！")


def pack_android_staging():
    tool.log("Android Staging 开始打包...")
    os.system("cd android && ./gradlew clean")
    os.system("cd android && ./gradlew assembleStaging")
    tool.log("Android Staging 打包结束！")


def pack_android_release():
    tool.log("Android Release 开始打包...")
    os.system("cd android && ./gradlew clean")
    os.system("cd android && ./gradlew assembleRelease")
    tool.log("Android Release 打包结束！")


def pack_ios_debug():
    print "pack_ios_debug"


def pack_ios_staging():
    print "pack_ios_staging"


def pack_ios_release():
    print "pack_ios_release"

