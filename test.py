from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtCore import QRect, Qt

from utils.ui.func import *
from XJ_AbstractCropper import *

import sys


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 500)
        self.setMouseTracking(True)

        # 图像展示框架
        self.img_frame = [0, 0, 200, 200]
        # 图像持有点
        self.img_hold_point = [0, 0]

        # 框选区域框架
        self.crop_frame = [0, 0, 0, 0]
        # 框架持有点
        self.crop_hold_point = [0, 0]
        self.draw_crop_flag = False
        self.drawing_crop_flag = False
        self.exits_crop_flag = False

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
        if self.draw_crop_flag:
            print(self.crop_frame)
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
            print('中键按下')
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                self.img_hold_point[0] = x
                self.img_hold_point[1] = y

        # 左键按下
        if a0.button() == Qt.LeftButton:
            print('左键按下')
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                # 判断有无 crop 区域存在
                if not self.exits_crop_flag:
                    self.draw_crop_flag = True
                    self.drawing_crop_flag = True

                    self.crop_frame = [x, y, x + 1, y + 1]

    """ 鼠标移动事件 """
    def mouseMoveEvent(self, a0):
        x = a0.pos().x()
        y = a0.pos().y()

        # 中键按下移动
        if a0.buttons() & Qt.MidButton:
            # 更新图像框的左上角坐标
            self.img_frame[0] += x - self.img_hold_point[0]
            self.img_frame[1] += y - self.img_hold_point[1]

            # 更新剪切框坐标
            if self.exits_crop_flag:
                self.crop_frame[0] += x - self.img_hold_point[0]
                self.crop_frame[1] += y - self.img_hold_point[1]
                self.crop_frame[2] += x - self.img_hold_point[0]
                self.crop_frame[3] += y - self.img_hold_point[1]

            # 更新图像持有点
            self.img_hold_point[0] = x
            self.img_hold_point[1] = y

        # 左键按下移动
        if a0.buttons() & Qt.LeftButton:
            if not self.exits_crop_flag and self.draw_crop_flag:

                # 点不在图像框中
                if x < self.img_frame[0]:
                    self.crop_frame[2] = self.img_frame[0]
                elif x > self.img_frame[0] + self.img_frame[2]:
                    self.crop_frame[2] = self.img_frame[0] + self.img_frame[2]
                else:
                    self.crop_frame[2] = x

                if y < self.img_frame[1]:
                    self.crop_frame[3] = self.img_frame[1]
                elif y > self.img_frame[1] + self.img_frame[3]:
                    self.crop_frame[3] = self.img_frame[1] + self.img_frame[3]
                else:
                    self.crop_frame[3] = y

        self.update()
        a0.accept()

    """ 鼠标升起事件 """
    def mouseReleaseEvent(self, a0):
        # 左键升起，move 不再响应左键
        if a0.button() == Qt.LeftButton and self.drawing_crop_flag:
            self.exits_crop_flag = True
            self.drawing_crop_flag = False
        self.update()
        a0.accept()

    """ 鼠标双击事件 """
    def mouseDoubleClickEvent(self, a0):
        # 右键双击
        if a0.button() == Qt.RightButton:
            # 还原 crop 坐标
            self.crop_frame = [0, 0, 0, 0]
            self.draw_crop_flag = False
            self.exits_crop_flag = False

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
            if self.exits_crop_flag:
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

