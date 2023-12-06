import cv2
import numpy as np

from PIL import Image


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
