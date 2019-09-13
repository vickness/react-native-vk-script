#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import imghdr


# 输出函数
def log(text):
    print '\033[32m' + text + '\033[0m'


# 检测 Image 是否安装
try:
    from PIL import Image, ImageDraw
except ImportError:
    log('缺少Image模块，正在安装Image模块，请等待...')
    success = os.system('python -m pip install Image')
    if success == 0:
        log('Image模块安装成功.')
        from PIL import Image, ImageDraw
    else:
        log('Image安装失败，请手动在终端执行：\'python -m pip install Image\'重新安装.')
        quit()


# 检查指定尺寸的图片是否存在
def image_size_exist(path, w, h):
    files = os.listdir(path)
    image_path = ""
    for name in files:
        # 读取图片
        file_path = os.path.join(path, name)
        # log(file_path)
        img_type = imghdr.what(file_path)
        if img_type == "png":
            image = Image.open(file_path)
            # 检测是否存在指定尺寸的图片
            if image.size[0] == w and image.size[1] == h:
                image_path = file_path

    return image_path


# 处理图片圆角
def circle_corner(image, radii):

    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    (w, h) = image.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', image.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    image.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return image
