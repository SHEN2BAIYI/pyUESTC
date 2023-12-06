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
