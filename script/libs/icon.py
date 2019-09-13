#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import tool
from PIL import Image, ImageDraw


# 当前工作目录
workPath = os.getcwd()


# icon图片尺寸
iosIconSize = ['20@2x', '20@3x', '29@2x', '29@3x', '40@2x', '40@3x', '60@2x', '60@3x', '1024@1x']
androidIconSize = [48, 72, 96, 144, 192]
androidNames = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']


# Android输出路径
androidIconOutPutPath = os.path.join(workPath, "android/app/src/main/res/")
# tool.log('android输出路径：%s' % androidIconOutPutPath)


# 遍历iOS工程路径，找到输出路径
iosIconOutPutPath = ""
for root, dirs, files in os.walk(os.path.join(workPath, "ios"), topdown=False):
    for name in dirs:
        if name.endswith("Images.xcassets"):
            iosIconOutPutPath = os.path.join(root, name, "AppIcon.appiconset/")
            # tool.log('ios输出路径：%s' % iosIconOutPutPath)

if len(iosIconOutPutPath) <= 0:
    tool.log('未找到 iOS 工程的 Images.xcassets')
    quit()


# 检查图片路径
def check_icon_path(path):

    if os.path.exists(path) is False:
        tool.log('输入路径无效: %s' % path)
        quit()

    # 检查icon输入路径是文件夹
    if os.path.isdir(path) is False:
        tool.log('请输入资源所在文件夹的路径')
        quit()

    # 获取图片地址
    image_path = tool.image_size_exist(path, 1024, 1024)
    if len(image_path) <= 0:
        tool.log('未找到尺寸 1024x1024 的 icon 图片')
        quit()

    # 返回图片完整地址
    return image_path


# 生成iOS的icon
def create_ios_icon(image_path):

    tool.log('开始配置 iOS 的 icon')

    # 创建icon文件夹
    if os.path.exists(iosIconOutPutPath) is False:
        os.makedirs(iosIconOutPutPath)
        # print '创建 ios 项目的 AppIcon.appiconset 文件夹'

    # 获取图片
    icon = Image.open(image_path).convert("RGBA")

    # 保存图片信息的列表
    image_list = []

    # 生成iOS图片，并保存到指定路径
    for size in iosIconSize:
        # 原始尺寸
        original_size = int(size.split('@')[0])
        # 图片倍数
        multiply = int(size.split('@')[1][0:1])
        # 生成图片
        im = icon.resize((original_size * multiply, original_size * multiply), Image.BILINEAR)
        # 图片完整名称
        name = "icon%s.png" % size
        # 保存到路径
        im.save(iosIconOutPutPath + name, "png")
        # 加入JSON文件
        image_list.append({
            "idiom": ("ios-marketing" if original_size == 1024 else "iphone"),
            "size": "%dx%d" % (original_size, original_size),
            "filename": name,
            "scale": "%dx" % multiply
        })

    # 创建 content 文件
    content = {
        "images": image_list,
        "info": {
            "version": 1,
            "author": "xcode"
        }
    }

    # 打开文件，写入json数据
    f = open(iosIconOutPutPath + 'Contents.json', 'w')
    f.write(json.dumps(content))

    tool.log('iOS icon 配置完成')


# 生成Android的icon
def create_android_icon(image_path):

    tool.log('开始配置 Android 的 icon')

    # 获取图片
    icon = Image.open(image_path).convert("RGBA")

    # 生成Android圆形icon
    circle_icon = tool.circle_corner(icon, radii=1024/2)
    index = 0
    for size in androidIconSize:
        # 压缩图片
        circle_im = circle_icon.resize((size, size), Image.BILINEAR)
        # 创建不同分辨率文件夹
        dir_path = "%s/mipmap-%s" % (androidIconOutPutPath, androidNames[index])
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
            # print '创建 %s' % dir_path

        # 保存到路径
        file_path = "%s/ic_launcher_round.png" % dir_path
        circle_im.save(file_path, "png")
        index = index + 1

    # 生成Android圆角矩形icon
    round_icon = tool.circle_corner(icon, radii=180)
    index = 0
    for size in androidIconSize:
        # 压缩图片
        round_im = round_icon.resize((size, size), Image.BILINEAR)
        # 创建不同分辨率文件夹
        dir_path = "%s/mipmap-%s" % (androidIconOutPutPath, androidNames[index])
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
            # print '创建 %s' % dir_path

        # 保存到路径
        file_path = "%s/ic_launcher.png" % dir_path
        round_im.save(file_path, "png")
        index = index + 1

    tool.log('Android icon 配置完成')
