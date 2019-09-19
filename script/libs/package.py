#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import tool
import shutil
import json

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 当前工作目录
workPath = os.getcwd()

# iOS项目路径
iosPath = os.path.join(workPath, "ios")

# ios App 生成地址
iosAppPath = os.path.join(workPath, "ios/build/apps")

# android App 生成地址
androidAppPath = os.path.join(workPath, "android/app/build/outputs/apk")

# app 输出地址
appFinalPath = os.path.join(workPath, "exports/apps")

# 查询ios项目名称
ios_project_name = ""
ios_workspace_name = ""

for name in os.listdir(iosPath):
    # print name
    if name.endswith("xcworkspace"):
        ios_workspace_name = name
    if name.endswith("xcodeproj"):
        ios_project_name = name

if len(ios_project_name) <= 0 and len(ios_workspace_name) <= 0:
    tool.log("未找到 iOS 工程")
    quit()

# iOS 打包目标名称
if len(ios_workspace_name) > 0:
    ios_scheme = ios_workspace_name
else:
    ios_scheme = ios_project_name

items = ios_scheme.split(".")
ios_scheme = items[0]
# print ios_scheme


# 读取json文件
with open(os.path.join(workPath, "exports/script.json"), "r+") as f:
    data = json.load(f)
    # 当前版本号
    version = data["version"]
    # app渠道
    channel = data["channel"]


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


def pack_workspace(mode):

    # iOS app 输出路径
    export_ipa_path = os.path.join(iosPath, "build/apps/%s" % mode)

    # iOS app 编译路径
    archive_path = os.path.join(iosPath, "build/xcarchive/%s.xcarchive" % mode)

    # 打包配置文件路径
    export_options_path = os.path.join(iosPath, "exports/options/%s.plist" % mode)

    if not os.path.isfile(export_options_path):
        tool.log("exports/options/%s.plist 文件不存在，请手动打一次包生成 ExportOptions.plist 文件，放入 exports/options 目录下" % mode)
        quit()

    tool.log("iOS清理")
    os.system("cd ios && xcodebuild clean "
              "-project %s "
              "-scheme %s "
              "-configuration %s "
              "-quiet || exit"
              % (
                  ios_workspace_name,
                  ios_scheme,
                  mode
              ))

    tool.log("iOS编译打包")
    os.system("cd ios && xcodebuild archive "
              "-project %s "
              "-scheme %s "
              "-configuration %s "
              "-archivePath %s "
              "-quiet || exit"
              % (
                  ios_workspace_name,
                  ios_scheme,
                  mode,
                  archive_path
              ))

    tool.log("iOS导出ipa")
    os.system("cd ios && xcodebuild -exportArchive "
              "-archivePath %s "
              "-exportPath %s "
              "-exportOptionsPlist %s "
              "-quiet || exit"
              % (
                  archive_path,
                  export_ipa_path,
                  export_options_path
              ))


def pack_project(mode):

    # iOS app 输出路径
    export_ipa_path = os.path.join(iosPath, "build/apps/%s" % mode)

    # iOS app 编译路径
    archive_path = os.path.join(iosPath, "build/xcarchive/%s.xcarchive" % mode)

    # 打包配置文件路径
    export_options_path = os.path.join(iosPath, "exports/options/%s.plist" % mode)

    if not os.path.isfile(export_options_path):
        tool.log("exports/options/%s.plist 文件不存在，请手动打一次包生成 ExportOptions.plist 文件，放入 exports/options 目录下" % mode)
        quit()

    tool.log("iOS清理")
    os.system("cd ios && xcodebuild clean "
              "-project %s "
              "-scheme %s "
              "-configuration %s "
              "-quiet || exit"
              % (
                  ios_project_name,
                  ios_scheme,
                  mode
              ))

    tool.log("iOS编译打包")
    os.system("cd ios && xcodebuild archive "
              "-project %s "
              "-scheme %s "
              "-configuration %s "
              "-archivePath %s "
              "-quiet || exit"
              % (
                  ios_project_name,
                  ios_scheme,
                  mode,
                  archive_path
              ))

    tool.log("iOS导出ipa")
    os.system("cd ios && xcodebuild -exportArchive "
              "-archivePath %s "
              "-exportPath %s "
              "-exportOptionsPlist %s "
              "-quiet || exit"
              % (
                  archive_path,
                  export_ipa_path,
                  export_options_path
              ))


def pack_ios_debug():
    # print "pack_ios_debug"
    if len(ios_workspace_name) > 0:
        pack_workspace("Debug")
    else:
        pack_project("Debug")


def pack_ios_staging():
    # print "pack_ios_staging"
    if len(ios_workspace_name) > 0:
        pack_workspace("Staging")
    else:
        pack_project("Staging")


def pack_ios_release():
    # print "pack_ios_release"
    if len(ios_workspace_name) > 0:
        pack_workspace("Release")
    else:
        pack_project("Release")


def remove_apps():

    shutil.rmtree(appFinalPath)
    os.mkdir(appFinalPath)

    # 遍历iOS工程路径，找ipa路径
    for root, dirs, files in os.walk(iosAppPath, topdown=False):
        for name in files:
            if name.endswith(".ipa"):
                path = os.path.join(root, name)
                print(path)

                # 重命名，并移动文件
                if "staging" in name:
                    new_path = "%s/%s_ios_%s_staging.ipa" % (appFinalPath, channel, version)
                    shutil.move(path, new_path)
                if "release" in name:
                    new_path = "%s/%s_ios_%s_release.ipa" % (appFinalPath, channel, version)
                    shutil.move(path, new_path)

    # 遍历Android工程路径，找ipa路径
    for root, dirs, files in os.walk(androidAppPath, topdown=False):
        for name in files:
            if name.endswith(".apk"):
                path = os.path.join(root, name)
                # print(path)
                shutil.move(path, appFinalPath)


