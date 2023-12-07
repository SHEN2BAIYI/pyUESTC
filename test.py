from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtCore import QRect, Qt

from utils.ui.func import *
from XJ_AbstractCropper import *

import sys
import numpy as np


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 500)
        self.setMouseTracking(True)

        # 图像展示框架
        self.img_frame = [0, 0, 200, 200]
        # 图像持有点
        self.img_hold_point = [0, 0]
        self.img_click_flag = True

        # 框选区域框架
        self.crop_frame = [0, 0, 0, 0]
        # 框架持有点
        self.crop_hold_point = [0, 0]
        self.crop_exits_flag = False                          # crop 区域存在标志
        self.crop_click_flag = False                          # crop 区域点击标志
        self.crop_change_flag = [False, False, False, False]  # crop 区域改变标志

        self.__fg = QImage('./dataset/Kaggle/archive/69_2.jpg')
        self.update()

    def set_img(self):
        self.__fg = QImage('./dataset/Kaggle/archive/69_2.jpg')
        self.update()

    """ 绘画事件 """
    def paintEvent(self, a0):
        painter = QPainter(self)

        # 绘制图片
        q_rect = QRect(self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3])
        painter.drawImage(q_rect, self.__fg)

        # 画线
        if np.array(self.crop_frame).any():
            # 如果存在 crop 区域，将坐标转换成左上角和右下角
            if self.crop_exits_flag:
                self.crop_frame = any2ltwh(self.crop_frame)

            # 限制在图像框内
            self.crop_frame[0] = limit_num_in_range(self.crop_frame[0], self.img_frame[0], self.img_frame[0] + self.img_frame[2])
            self.crop_frame[1] = limit_num_in_range(self.crop_frame[1], self.img_frame[1], self.img_frame[1] + self.img_frame[3])
            self.crop_frame[2] = limit_num_in_range(self.crop_frame[2], self.img_frame[0], self.img_frame[0] + self.img_frame[2])
            self.crop_frame[3] = limit_num_in_range(self.crop_frame[3], self.img_frame[1], self.img_frame[1] + self.img_frame[3])

            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(self.crop_frame[0], self.crop_frame[1], self.crop_frame[0], self.crop_frame[3])
            painter.drawLine(self.crop_frame[0], self.crop_frame[1], self.crop_frame[2], self.crop_frame[1])
            painter.drawLine(self.crop_frame[2], self.crop_frame[3], self.crop_frame[2], self.crop_frame[1])
            painter.drawLine(self.crop_frame[2], self.crop_frame[3], self.crop_frame[0], self.crop_frame[3])

    """ 鼠标点击事件 """
    def mousePressEvent(self, a0):
        x = a0.pos().x()
        y = a0.pos().y()

        # 中键按下
        if a0.button() == Qt.MidButton:
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                # 点击正确位置，图像可以移动
                self.img_click_flag = True
                # 更新图像持有点
                self.img_hold_point[0] = x
                self.img_hold_point[1] = y

        # 左键按下
        if a0.button() == Qt.LeftButton:
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                # 判断有无 crop 区域存在
                # 无 cope 区域存在，本次目标在于创建 crop 区域
                if not self.crop_exits_flag:
                    self.crop_click_flag = True

                    self.crop_frame = [x, y, x + 1, y + 1]

                else:
                    # 有 crop 区域，判断点是否在 crop 框中
                    # 在 crop 框中，本次目标在于移动 crop 框或改变 crop 框大小
                    if is_in_frame(x, y,
                                   min(self.crop_frame[0], self.crop_frame[2]),
                                   min(self.crop_frame[1], self.crop_frame[3]),
                                   abs(self.crop_frame[2] - self.crop_frame[0]),
                                   abs(self.crop_frame[3] - self.crop_frame[1])):
                        self.crop_click_flag = True

                        # 提取 crop 点击点
                        self.crop_hold_point[0] = x
                        self.crop_hold_point[1] = y

                        # 判断点击点在 crop 框的哪个位置
                        self.crop_change_flag = point_in_frame(x, y,
                                                               self.crop_frame[0], self.crop_frame[1],
                                                               self.crop_frame[2] - self.crop_frame[0],
                                                               self.crop_frame[3] - self.crop_frame[1])

    """ 鼠标移动事件 """
    def mouseMoveEvent(self, a0):
        x = a0.pos().x()
        y = a0.pos().y()

        # 中键按下移动
        if a0.buttons() & Qt.MidButton and self.img_click_flag:
            # 更新图像框的左上角坐标
            self.img_frame[0] += x - self.img_hold_point[0]
            self.img_frame[1] += y - self.img_hold_point[1]

            # 更新剪切框坐标
            if self.crop_exits_flag:
                self.crop_frame[0] += x - self.img_hold_point[0]
                self.crop_frame[1] += y - self.img_hold_point[1]
                self.crop_frame[2] += x - self.img_hold_point[0]
                self.crop_frame[3] += y - self.img_hold_point[1]

            # 更新图像持有点
            self.img_hold_point[0] = x
            self.img_hold_point[1] = y

        # 左键按下移动
        if a0.buttons() & Qt.LeftButton:
            # 不存在裁剪框，但是点击了正确的位置，目标在于创建裁剪框
            if not self.crop_exits_flag and self.crop_click_flag:

                # 点不在图像框中
                self.crop_frame[2] = limit_num_in_range(x, self.img_frame[0], self.img_frame[0] + self.img_frame[2])
                self.crop_frame[3] = limit_num_in_range(y, self.img_frame[1], self.img_frame[1] + self.img_frame[3])

            # 存在裁剪框, 目标在于移动裁剪框或改变裁剪框大小
            elif self.crop_exits_flag and self.crop_click_flag:
                # 更新裁剪框坐标
                for index, flag in enumerate(self.crop_change_flag):
                    if flag and index % 2 == 0:
                        self.crop_frame[index] += x - self.crop_hold_point[0]
                    if flag and index % 2 == 1:
                        self.crop_frame[index] += y - self.crop_hold_point[1]

                # 更新裁剪框持有点
                self.crop_hold_point[0] = x
                self.crop_hold_point[1] = y

        # 平常移动，设置鼠标样式
        if self.crop_exits_flag:
            if is_in_frame(x, y,
                           self.crop_frame[0], self.crop_frame[1],
                           self.crop_frame[2] - self.crop_frame[0],
                           self.crop_frame[3] - self.crop_frame[1]):

                flags = point_in_frame(x, y,
                                       self.crop_frame[0], self.crop_frame[1],
                                       self.crop_frame[2] - self.crop_frame[0],
                                       self.crop_frame[3] - self.crop_frame[1])

                # 设置中间鼠标样式
                if flags[0] and flags[1] and flags[2] and flags[3]:
                    self.setCursor(Qt.SizeAllCursor)
                # 设置左上角鼠标样式
                elif flags[0] and flags[1]:
                    self.setCursor(Qt.SizeFDiagCursor)
                # 设置右上角鼠标样式
                elif flags[2] and flags[1]:
                    self.setCursor(Qt.SizeBDiagCursor)
                # 设置左下角鼠标样式
                elif flags[0] and flags[3]:
                    self.setCursor(Qt.SizeBDiagCursor)
                # 设置右下角鼠标样式
                elif flags[2] and flags[3]:
                    self.setCursor(Qt.SizeFDiagCursor)
                # 设置上边鼠标样式
                elif flags[1]:
                    self.setCursor(Qt.SizeVerCursor)
                # 设置下边鼠标样式
                elif flags[3]:
                    self.setCursor(Qt.SizeVerCursor)
                # 设置左边鼠标样式
                elif flags[0]:
                    self.setCursor(Qt.SizeHorCursor)
                # 设置右边鼠标样式
                elif flags[2]:
                    self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        self.update()
        a0.accept()

    """ 鼠标升起事件 """
    def mouseReleaseEvent(self, a0):
        # 左键升起，不管目标如何，只要点击了正确位置，则会存在 crop 区域
        if a0.button() == Qt.LeftButton and self.crop_click_flag:
            self.crop_exits_flag = True
            self.crop_click_flag = False
            self.crop_change_flag = [False, False, False, False]

        # 中键升起，move 不再响应中键
        if a0.button() == Qt.MidButton:
            self.img_click_flag = False

        self.update()
        a0.accept()

    """ 鼠标双击事件 """
    def mouseDoubleClickEvent(self, a0):
        # 右键双击
        if a0.button() == Qt.RightButton:
            # 还原 crop 坐标
            self.crop_frame = [0, 0, 0, 0]
            self.crop_exits_flag = False

    """ 滚轮滚动事件 """
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
            self.img_frame[0] = int(x - (x - self.img_frame[0]) * scale)
            self.img_frame[1] = int(y - (y - self.img_frame[1]) * scale)
            self.img_frame[2] = int(self.img_frame[2] * scale)
            self.img_frame[3] = int(self.img_frame[3] * scale)

            # 更新剪切框坐标
            if self.crop_exits_flag:
                self.crop_frame[0] = int(x - (x - self.crop_frame[0]) * scale)
                self.crop_frame[1] = int(y - (y - self.crop_frame[1]) * scale)
                self.crop_frame[2] = int(x - (x - self.crop_frame[2]) * scale)
                self.crop_frame[3] = int(y - (y - self.crop_frame[3]) * scale)

        self.update()
        a0.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = Test()
    test.show()
    test.set_img()

    sys.exit(app.exec())

