from utils.ui.func import *
from ui.basic import CropperWindow

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
import sys
import numpy as np

class ImageCropper(QWidget, CropperWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(1000, 500)
        self.setMouseTracking(True)
        self.imgFrame.setMouseTracking(True)
        self.imgLabel.setMouseTracking(True)
        self.imgLabel.setPixmap(
            QPixmap(self.imgLabel.width(), self.imgLabel.height())
        )

        """ 图像操作 Frame """
        # 图像展示框架
        self.img_frame = [0, 0, 0, 0]
        self.img_path = None
        # 图像持有点
        self.img_hold_point = [0, 0]
        self.img_click_flag = False

        # 框选区域框架
        self.crop_frame = [0, 0, 0, 0]
        # 框架持有点
        self.crop_hold_point = [0, 0]
        self.crop_exits_flag = False                          # crop 区域存在标志
        self.crop_click_flag = False                          # crop 区域点击标志
        self.crop_change_flag = [False, False, False, False]  # crop 区域改变标志

        # 图像 QImage 本身
        self.__fg = None

        """ 控制界面 Frame """
        self.cwd = os.getcwd()
        self.store_list = []

        self.__init_bind_event()

    """ 初始化主页面绑定事件 """
    def __init_bind_event(self):
        # 绑定微调按钮事件
        self.topUpButton.clicked.connect(lambda: self.__adjust_crop(1, -1))
        self.topDownButton.clicked.connect(lambda: self.__adjust_crop(1, 1))
        self.leftUpButton.clicked.connect(lambda: self.__adjust_crop(0, -1))
        self.leftDownButton.clicked.connect(lambda: self.__adjust_crop(0, 1))
        self.rightUpButton.clicked.connect(lambda: self.__adjust_crop(2, -1))
        self.rightDownButton.clicked.connect(lambda: self.__adjust_crop(2, 1))
        self.bottomUpButton.clicked.connect(lambda: self.__adjust_crop(3, -1))
        self.bottomDownButton.clicked.connect(lambda: self.__adjust_crop(3, 1))

        # 绑定文件夹选择事件
        self.storeLineEdit.mouseDoubleClickEvent = self.__choose_file

        # 绑定保存按钮事件
        self.storeButton.clicked.connect(self.__save_crop)

    """ 初始化保存列表 """
    def __init_store_list(self):
        if not self.storeLineEdit.text():
            return

        # 读取路径下所有图片文件
        # 读取文件夹下的文件
        files = os.listdir(self.storeLineEdit.text())
        files = [x for x in files if x.endswith('.jpg') or x.endswith('.png')]
        list_model = QStringListModel()
        list_model.setStringList(files)

        self.storeListView.setModel(list_model)
        self.storeListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    ########################
    #       功能性函数       #
    ########################
    def reset(self):
        # 图像展示框架
        self.img_frame = [0, 0, 0, 0]
        self.img_path = None
        # 图像持有点
        self.img_hold_point = [0, 0]
        self.img_click_flag = False

        # 框选区域框架
        self.crop_frame = [0, 0, 0, 0]
        # 框架持有点
        self.crop_hold_point = [0, 0]
        self.crop_exits_flag = False  # crop 区域存在标志
        self.crop_click_flag = False  # crop 区域点击标志
        self.crop_change_flag = [False, False, False, False]  # crop 区域改变标志

    """ 设置图像 """
    def set_img(self, img_path):
        self.img_path = img_path
        self.__fg = QImage(img_path)
        self.img_frame = [50, 50, self.__fg.width(), self.__fg.height()]
        self.update()

    """ 保存裁剪图像（并进行坐标同步） """
    def __save_crop(self):
        if not self.crop_exits_flag or not self.storeLineEdit.text():
            QMessageBox.warning(self, '警告', '请检查保存路径或者是否存在 crop 区域！')
            return

        # 将 crop 区域转换到原图像中
        img_frame = self.img_frame.copy()
        crop_frame = self.crop_frame.copy()
        # 加载原图像
        img = cv2.imread(self.img_path)

        # 计算比例
        x1 = round((crop_frame[0] - img_frame[0]) * img.shape[1] / img_frame[2])
        y1 = round((crop_frame[1] - img_frame[1]) * img.shape[0] / img_frame[3])

        x2 = round((crop_frame[2] - img_frame[0]) * img.shape[1] / img_frame[2])
        y2 = round((crop_frame[3] - img_frame[1]) * img.shape[0] / img_frame[3])

        # 保存图像
        img = img[y1:y2, x1:x2]
        # 拆分图像路径
        _, file_name = os.path.split(self.img_path)
        file_path = self.storeLineEdit.text()
        # 判断 file_path 文件夹是否存在
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, file_name)

        cv2.imwrite(file_path, img)
        # 显示保存记录
        self.__init_store_list()
        QMessageBox.information(self, '提示', '保存成功！')

    """ 选择目录 """
    def __choose_file(self, *args):
        file_name = QFileDialog.getExistingDirectory(self, "选取文件夹", self.cwd)

        # 选择文件夹并传递给 line_edit
        if file_name:
            self.storeLineEdit.setText(file_name)
            self.__init_store_list()

    """ 微调 crop 区域 """
    def __adjust_crop(self, target, step=1):
        # 获取当前 crop 区域
        crop = self.crop_frame.copy()

        # 根据 target 选择 index。上(1)下(3)左(0)右(2)
        crop[target] += step

        self.crop_frame = crop
        self.update()

    ########################
    #      窗口监听事件      #
    ########################
    """ 绘画事件 """
    def paintEvent(self, a0):
        self.imgLabel.pixmap().fill(QColor(249, 249, 249))
        painter = QPainter(self.imgLabel.pixmap())

        # 偏置修正
        bias_x = -20
        bias_y = -20

        # bias_x = self.imgLabel.x() - self.imgFrame.x()
        # bias_y = self.imgLabel.y() - self.imgFrame.y()

        if self.__fg:
            # 绘制图片
            # painter.drawImage(self.imgFrame.rect(), self.__fg)
            # self.label.setGeometry(QRect(self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]))
            q_rect = QRect(self.img_frame[0] + bias_x, self.img_frame[1] + bias_y, self.img_frame[2], self.img_frame[3])
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
                painter.drawLine(self.crop_frame[0] + bias_x, self.crop_frame[1] + bias_y,
                                 self.crop_frame[0] + bias_x, self.crop_frame[3] + bias_y)
                painter.drawLine(self.crop_frame[0] + bias_x, self.crop_frame[1] + bias_y,
                                 self.crop_frame[2] + bias_x, self.crop_frame[1] + bias_y)
                painter.drawLine(self.crop_frame[2] + bias_x, self.crop_frame[3] + bias_y,
                                 self.crop_frame[2] + bias_x, self.crop_frame[1] + bias_y)
                painter.drawLine(self.crop_frame[2] + bias_x, self.crop_frame[3] + bias_y,
                                 self.crop_frame[0] + bias_x, self.crop_frame[3] + bias_y)

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
            self.img_frame[0] = round(x - (x - self.img_frame[0]) * scale)
            self.img_frame[1] = round(y - (y - self.img_frame[1]) * scale)
            self.img_frame[2] = round(self.img_frame[2] * scale)
            self.img_frame[3] = round(self.img_frame[3] * scale)

            # 更新剪切框坐标
            if self.crop_exits_flag:
                self.crop_frame[0] = round(x - (x - self.crop_frame[0]) * scale)
                self.crop_frame[1] = round(y - (y - self.crop_frame[1]) * scale)
                self.crop_frame[2] = round(x - (x - self.crop_frame[2]) * scale)
                self.crop_frame[3] = round(y - (y - self.crop_frame[3]) * scale)

        self.update()
        a0.accept()







