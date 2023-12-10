import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils.ui.func import *


class ImageController(QWidget):
    def __init__(self):
        super(ImageController, self).__init__()
        self.setMouseTracking(True)     # 跟踪鼠标

        """ 图像操作 """
        # 图像展示框架
        self.img_frame = [0, 0, 0, 0]
        self.img_path = None
        # 图像持有点
        self.img_hold_point = [0, 0]
        self.img_click_flag = False
        # 图像 QImage
        self.__fg = None

    """ 重置 """
    def reset(self):
        self.img_frame = [0, 0, 0, 0]
        self.img_path = None
        self.img_hold_point = [0, 0]
        self.img_click_flag = False

    """ 设置图像 """
    def set_img(self, img_path):
        self.img_path = img_path
        self.__fg = QImage(img_path)
        self.img_frame = [0, 0, self.__fg.width(), self.__fg.height()]
        self.update()

    """ 重写 paintEvent """
    def paintEvent(self, event):
        if not self.__fg:
            return

        painter = QPainter(self)
        # 绘制图片
        self.bg.setRect(self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3])
        painter.drawImage(self.bg, self.fg)

    """ 重写 mousePressEvent """
    def mousePressEvent(self, event):
        if not self.__fg:
            return

        x = event.pos().x()
        y = event.pos().y()

        # 中键按下
        if event.button() == Qt.MidButton:
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                # 点击正确位置，图像可以移动
                self.img_click_flag = True
                # 更新图像持有点
                self.img_hold_point[0] = x
                self.img_hold_point[1] = y

    """ 重写 mouseMoveEvent """
    def mouseMoveEvent(self, event):
        if not self.__fg:
            return

        x = event.pos().x()
        y = event.pos().y()

        # 中键按下移动
        if event.buttons() & Qt.MidButton and self.img_click_flag:
            # 更新图像框的左上角坐标
            self.img_frame[0] += x - self.img_hold_point[0]
            self.img_frame[1] += y - self.img_hold_point[1]

            # 更新图像持有点
            self.img_hold_point[0] = x
            self.img_hold_point[1] = y

        self.update()
        event.accept()

    """ 重写 mouseReleaseEvent """
    def mouseReleaseEvent(self, a0):
        # 中键升起，move 不再响应中键
        if a0.button() == Qt.MidButton:
            self.img_click_flag = False

        self.update()
        a0.accept()

    """ 重写 wheelEvent """
    def wheelEvent(self, a0):
        x = a0.pos().x()
        y = a0.pos().y()

        # 判断点是否在图像框中
        if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
            # 根据滚动角度放大缩小
            if a0.angleDelta().y() > 0:
                scale = 1.2
            else:
                scale = 0.8

            # 更新图像坐标
            self.img_frame[0] = round(x - (x - self.img_frame[0]) * scale)
            self.img_frame[1] = round(y - (y - self.img_frame[1]) * scale)
            self.img_frame[2] = round(self.img_frame[2] * scale)
            self.img_frame[3] = round(self.img_frame[3] * scale)

        self.update()
        a0.accept()
