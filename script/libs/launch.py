#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import json
import tool
from PIL import Image, ImageDraw
import imghdr

# 编码转化
reload(sys)
sys.setdefaultencoding('utf-8')

# 启动图尺寸
iosSplashSize = [(320, 480), (640, 960), (640, 1136), (750, 1334), (828, 1792), (1125, 2436), (1242, 2208), (1242, 2688)]
androidSplashSize = [(320, 480), (480, 800), (720, 1280), (960, 1600), (1280, 1920)]
androidNames = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']


# 必要尺寸
splashSize = [(640, 1136), (720, 1280), (750, 1334), (828, 1792), (960, 1600), (1125, 2436), (1242, 2208), (1242, 2688), (1280, 1920)]


# 当前工作目录
workPath = os.getcwd()


# Android输出路径
androidSplashOutPutPath = os.path.join(workPath, "android/app/src/main/res/")


# 遍历iOS工程路径，找到输出路径
iosSplashOutPutPath = ""
for root, dirs, files in os.walk(os.path.join(workPath, "ios"), topdown=False):
    for name in dirs:
        if name.endswith("Images.xcassets"):
            iosSplashOutPutPath = os.path.join(root, name, "LaunchImage.launchimage/")
            # tool.log('ios输出路径：%s' % iosSplashOutPutPath)

if len(iosSplashOutPutPath) <= 0:
    tool.log('未找到 iOS 工程的 Images.xcassets')
    quit()


# ios 启动图配置文件
splash_content = {
    "images": [
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "2688h",
            "filename": "launch1242x2688.png",
            "minimum-system-version": "12.0",
            "orientation": "portrait",
            "scale": "3x"
        },
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "1792h",
            "filename": "launch828x1792.png",
            "minimum-system-version": "12.0",
            "orientation": "portrait",
            "scale": "2x"
        },
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "2436h",
            "filename": "launch1125x2436.png",
            "minimum-system-version": "11.0",
            "orientation": "portrait",
            "scale": "3x"
        },
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "736h",
            "filename": "launch1242x2208.png",
            "minimum-system-version": "8.0",
            "orientation": "portrait",
            "scale": "3x"
        },
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "667h",
            "filename": "launch750x1334.png",
            "minimum-system-version": "8.0",
            "orientation": "portrait",
            "scale": "2x"
        },
        {
            "orientation": "portrait",
            "idiom": "iphone",
            "filename": "launch640x960.png",
            "extent": "full-screen",
            "minimum-system-version": "7.0",
            "scale": "2x"
        },
        {
            "extent": "full-screen",
            "idiom": "iphone",
            "subtype": "retina4",
            "filename": "launch640x1136.png",
            "minimum-system-version": "7.0",
            "orientation": "portrait",
            "scale": "2x"
        },
        {
            "orientation": "portrait",
            "idiom": "iphone",
            "filename": "launch320x480.png",
            "extent": "full-screen",
            "scale": "1x"
        },
        {
            "orientation": "portrait",
            "idiom": "iphone",
            "filename": "launch640x960.png",
            "extent": "full-screen",
            "scale": "2x"
        },
        {
            "orientation": "portrait",
            "idiom": "iphone",
            "filename": "launch640x1136.png",
            "extent": "full-screen",
            "subtype": "retina4",
            "scale": "2x"
        }
    ],
    "info": {
        "version": 1,
        "author": "xcode"
    }
}


# 检查splash图片尺寸是否完整
def check_splash_path(path):

    if os.path.exists(path) is False:
        tool.log('输入路径无效: %s' % path)
        quit()

    # 检查icon输入路径是文件夹
    if os.path.isdir(path) is False:
        tool.log('请输入资源所在文件夹的路径')
        quit()

    # 遍历必要尺寸
    is_exist = True
    for (w, h) in splashSize:
        image_path = tool.image_size_exist(path, w, h)
        if len(image_path) <= 0:
            tool.log('尺寸 %dx%d 的启动图不存在' % (w, h))
            is_exist = False

    if is_exist is False:
        quit()


# 生成iOS的启动图
def create_ios_splash(path):

    tool.log('开始配置 iOS Splash')

    # 创建启动图文件夹
    if os.path.exists(iosSplashOutPutPath) is False:
        os.makedirs(iosSplashOutPutPath)
        # print '创建 ios LaunchImage.launchimage 文件夹'

    # 获取所有文件
    files = os.listdir(path)

    # 遍历所有文件
    for file_name in files:
        file_path = os.path.join(path, file_name)
        img_type = imghdr.what(file_path)
        # 找出png格式的图片
        if img_type == "png":
            image = Image.open(file_path)
            if image.size in iosSplashSize:
                w = image.size[0]
                h = image.size[1]
                # 图片完整名称
                name = "launch%dx%d.png" % (w, h)
                # print name
                # 保存到路径
                image.save(iosSplashOutPutPath + name, "png")

                # 图片尺寸缩小一半，在尺寸列表中
                if (w/2, h/2) in iosSplashSize:
                    # 图片完整名称
                    name = "launch%dx%d.png" % (w/2, h/2)
                    # print name
                    # 生成图片
                    im = image.resize((w/2, h/2), Image.BILINEAR)
                    # 保存到路径
                    im.save(iosSplashOutPutPath + name, "png")

    # 打开文件，写入json数据
    f = open(iosSplashOutPutPath + 'Contents.json', 'w')
    f.write(json.dumps(splash_content))

    tool.log('iOS Splash 配置完成')


# 生成Android的启动图
def create_android_splash(path):

    tool.log('开始配置 Android Splash')

    # 获取文件夹下所有图片
    files = os.listdir(path)

    # 遍历文件图片
    for file_name in files:

        file_path = os.path.join(path, file_name)
        img_type = imghdr.what(file_path)
        # 找出png格式的图片
        if img_type == "png":
            image = Image.open(file_path)
            # 找出指定文件的位置
            if image.size in androidSplashSize:
                w = image.size[0]
                h = image.size[1]
                index = androidSplashSize.index(image.size)
                # 创建不同分辨率文件夹
                dir_path = "%sdrawable-%s" % (androidSplashOutPutPath, androidNames[index])
                if os.path.exists(dir_path) is False:
                    os.makedirs(dir_path)
                    # print '创建 %s' % dir_path

                # 保存图片到路径
                file_path = "%s/launch_screen.png" % dir_path
                image.save(file_path, "png")
                # print file_path

                # 图片尺寸缩小一半，在尺寸列表中
                if (w/2, h/2) in androidSplashSize:
                    index = androidSplashSize.index((w/2, h/2))
                    # 创建不同分辨率文件夹
                    dir_path = "%sdrawable-%s" % (androidSplashOutPutPath, androidNames[index])
                    if os.path.exists(dir_path) is False:
                        os.makedirs(dir_path)
                        # print '创建 %s' % dir_path

                    # 保存图片到路径
                    file_path = "%s/launch_screen.png" % dir_path
                    # 生成图片
                    im = image.resize((w/2, h/2), Image.BILINEAR)
                    im.save(file_path, "png")
                    # print file_path

                # 图片尺寸缩小一半，在尺寸列表中
                if (w/4, h/4) in androidSplashSize:
                    index = androidSplashSize.index((w/4, h/4))
                    # 创建不同分辨率文件夹
                    dir_path = "%sdrawable-%s" % (androidSplashOutPutPath, androidNames[index])
                    if os.path.exists(dir_path) is False:
                        os.makedirs(dir_path)
                        # print '创建 %s' % dir_path

                    # 保存图片到路径
                    file_path = "%s/launch_screen.png" % dir_path
                    # 生成图片
                    im = image.resize((w/4, h/4), Image.BILINEAR)
                    im.save(file_path, "png")
                    # print file_path

    tool.log('Android Splash 配置完成')
