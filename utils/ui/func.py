import cv2
import numpy as np

from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


""" 生成马赛克背景图 """
def create_mosaic_bg(shape, color, interval):
    """
    :param shape: 生成背景图片的大小
    :param color: 生成背景图像的组成颜色（马赛克一般黑白交替）
    :param interval: 格子大小
    :return:
    """
    color0 = list(color[0])
    color1 = list(color[1])


""" 判断点是否在框中 """
def is_in_frame(point_x, point_y, frame_x, frame_y, frame_width, frame_height):
    if frame_x <= point_x <= frame_x + frame_width and frame_y <= point_y <= frame_y + frame_height:
        return True

    return False


""" 限制点在框中 """
def limit_num_in_range(num, min_num, max_num):
    if num < min_num:
        return min_num
    elif num > max_num:
        return max_num
    else:
        return num


""" 任何坐标转左上右下坐标 """
def any2ltwh(coords):
    assert len(coords) == 4
    return [min(coords[0], coords[2]), min(coords[1], coords[3]),
            max(coords[0], coords[2]), max(coords[1], coords[3])]


""" 点在框中的位置 """
def point_in_frame(point_x, point_y, frame_x, frame_y, frame_width, frame_height, padding=10):
    # 先对四角进行判定
    # 左上
    if is_in_frame(point_x, point_y, frame_x - padding, frame_y - padding, padding * 2, padding * 2):
        return [True, True, False, False]
    # 右上
    elif is_in_frame(point_x, point_y, frame_x + frame_width - padding, frame_y - padding, padding * 2, padding * 2):
        return [False, True, True, False]
    # 左下
    elif is_in_frame(point_x, point_y, frame_x - padding, frame_y + frame_height - padding, padding * 2, padding * 2):
        return [True, False, False, True]
    # 右下
    elif is_in_frame(point_x, point_y, frame_x + frame_width - padding, frame_y + frame_height - padding, padding * 2, padding * 2):
        return [False, False, True, True]
    # 再对四边进行判定
    # 上
    elif is_in_frame(point_x, point_y, frame_x, frame_y - padding, frame_width, padding * 2):
        return [False, True, False, False]
    # 下
    elif is_in_frame(point_x, point_y, frame_x, frame_y + frame_height - padding, frame_width, padding * 2):
        return [False, False, False, True]
    # 左
    elif is_in_frame(point_x, point_y, frame_x - padding, frame_y, padding * 2, frame_height):
        return [True, False, False, False]
    # 右
    elif is_in_frame(point_x, point_y, frame_x + frame_width - padding, frame_y, padding * 2, frame_height):
        return [False, False, True, False]

    return [True, True, True, True]



