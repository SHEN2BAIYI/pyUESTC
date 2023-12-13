"""
    Flaw Mask 的记录采用比例的形式进行记录，即：
        mask_point = [中心点x占比，中心点y占比，直径，当前图像width，当前图像height]
"""

from PyQt5.QtGui import *
import os
import math

from ImageTool.ui.basic import FlawRemoverWindow
from utils.ui.func import *
from utils.flaw_removal import *


class FlawRemover(QWidget, FlawRemoverWindow):
    def __init__(self):
        super(FlawRemover, self).__init__()
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

        # mask 点的记录 - (中心点x，中心点y，半径，当前图像x，当前图像y)
        self.radius = 20
        self.mask_point = [0, 0]
        self.mask_all_point = {}
        self.mask_now_point = []
        self.mask_click_flag = False

        # 图像 QImage 本身
        self.__fg = None

        """ 控制界面 Frame """
        self.cwd = os.getcwd()

        # 初始化
        self.__init_bind_event()

    def __init_bind_event(self):
        self.sizeSlider.valueChanged.connect(self.__change_radius)
        self.withdrawButton.clicked.connect(self.__undo)
        self.storeLineEdit.mouseDoubleClickEvent = self.__choose_file
        self.storeButton.clicked.connect(self.__save_mask)

        self.storeListView.doubleClicked.connect(self.__show_img)

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
    """ 重置 """
    def reset(self):
        self.img_frame = [0, 0, 0, 0]
        self.img_path = None
        self.img_hold_point = [0, 0]
        self.img_click_flag = False

        self.mask_point = [0, 0]
        self.mask_all_point = {}
        self.mask_now_point = []
        self.mask_click_flag = False

    """ 设置图像 """
    def set_img(self, img_path):
        self.img_path = img_path
        self.__fg = QImage(img_path)
        self.img_frame = [50, 50, self.__fg.width(), self.__fg.height()]
        self.update()

    """ 改变 mask 点的半径 """
    def __change_radius(self):
        self.radius = self.sizeSlider.value()
        self.update()

    """ 撤销一次 mask 绘制 """
    def __undo(self):
        if len(self.mask_all_point):
            self.mask_all_point.popitem()
            self.update()

    """ 选择保存文件夹 """
    def __choose_file(self, *args):
        file_name = QFileDialog.getExistingDirectory(self, "选取文件夹", self.cwd)

        # 选择文件夹并传递给 line_edit
        if file_name:
            self.storeLineEdit.setText(file_name)
            self.__init_store_list()

    """ 保存 mask """
    def __save_mask(self):
        # 检查
        if not self.storeLineEdit.text() or not len(self.mask_all_point):
            QMessageBox.warning(self, "警告", "请先选择保存路径或者绘制 mask！")
            return

        # 保存
        # 打开原图，得到图像大小
        img = cv2.imread(self.img_path)
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        img_height, img_width = img.shape[:2]
        for _, points in self.mask_all_point.items():
            for point in points:
                # 计算真实坐标
                point_x = math.ceil(point[0] * img_width)
                point_y = math.ceil(point[1] * img_height)

                # 记录 mask
                cv2.circle(
                    mask,
                    (point_x, point_y),
                    int(point[2] / point[3] * img_width / 2),
                    255, -1
                )

                cv2.circle(
                    img,
                    (point_x, point_y),
                    int(point[2] / point[3] * img_width / 2),
                    255, -1
                )

        # cv2.imshow("img", img)
        # cv2.imshow("mask", mask)

        new_mask = make_mask(mask)

        # 保存
        # 拆分图像路径
        _, file_name = os.path.split(self.img_path)
        file_path = self.storeLineEdit.text()
        # 判断 file_path 文件夹是否存在
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, file_name)
        cv2.imwrite(file_path, new_mask)

        finish_removal(self.img_path, file_path, img_width, img_height, file_path)

        # 设置保存列表
        self.__init_store_list()

    """ 展示图像 """
    def __show_img(self):
        # 获取文件名
        file_name = self.storeListView.selectionModel().selectedIndexes()[0].data()

        # 获取文件全路径
        file_path = os.path.join(self.storeLineEdit.text(), file_name)

        # 设置图像
        img = cv2.imread(file_path)
        cv2.imshow('img', img)

    ########################
    #       监听函数        #
    ########################
    """ 重写 paintEvent """
    def paintEvent(self, event):
        def do(my_point):
            # 按照比例计算真实坐标
            point_x = math.ceil(my_point[0] * self.img_frame[2] + self.img_frame[0])
            point_y = math.ceil(my_point[1] * self.img_frame[3] + self.img_frame[1])

            # 画图
            painter.drawEllipse(
                int(point_x + bias_x - self.img_frame[2] / my_point[3] * my_point[2] / 2),
                int(point_y + bias_y - self.img_frame[3] / my_point[4] * my_point[2] / 2),
                int(self.img_frame[2] / my_point[3] * my_point[2]),
                int(self.img_frame[3] / my_point[4] * my_point[2])
            )

        self.imgLabel.pixmap().fill(QColor(249, 249, 249))
        painter = QPainter(self.imgLabel.pixmap())

        # 偏置修正
        bias_x = -20
        bias_y = -20
        if self.__fg:
            # 绘制图片
            q_rect = QRect(self.img_frame[0] + bias_x, self.img_frame[1] + bias_y, self.img_frame[2], self.img_frame[3])
            painter.drawImage(q_rect, self.__fg)

            # 绘制 mask
            if self.mask_now_point or len(self.mask_all_point) or np.array(self.mask_point).any():
                # 先遍历 mask_now_point
                painter.setBrush(QColor(0, 0, 255, 64))
                painter.setPen(Qt.NoPen)

                for point in self.mask_now_point:
                    do(point)

                # 再遍历 mask_all_point
                for key in self.mask_all_point.keys():
                    for point in self.mask_all_point[key]:
                        do(point)

                # 最后遍历 mask_point
                if np.array(self.mask_point).any():
                    painter.drawEllipse(int(self.mask_point[0] + bias_x - self.radius / 2),
                                        int(self.mask_point[1] + bias_y - self.radius / 2),
                                        self.radius, self.radius)

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

        # 左键按下
        if event.button() == Qt.LeftButton:
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
                self.mask_click_flag = True
                self.mask_now_point.append(
                    [(x - self.img_frame[0])/self.img_frame[2],
                     (y - self.img_frame[1])/self.img_frame[3],
                     self.radius,
                     self.img_frame[2], self.img_frame[3]]
                )

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

        # 左键按下移动
        if event.buttons() & Qt.LeftButton:
            # 判断点是否在图像框中
            if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]) \
                    and self.mask_click_flag:
                self.mask_now_point.append(
                    [(x - self.img_frame[0])/self.img_frame[2],
                     (y - self.img_frame[1])/self.img_frame[3],
                     self.radius,
                     self.img_frame[2], self.img_frame[3]]
                )
        # 判断是否在图像框中
        if is_in_frame(x, y, self.img_frame[0], self.img_frame[1], self.img_frame[2], self.img_frame[3]):
            self.mask_point = [x, y]
        else:
            self.mask_point = [0, 0]

        self.update()
        event.accept()

    """ 重写 mouseReleaseEvent """
    def mouseReleaseEvent(self, a0):
        # 中键升起，move 不再响应中键
        if a0.button() == Qt.MidButton:
            self.img_click_flag = False

        # 左键升起，move 不再响应左键
        if a0.button() == Qt.LeftButton and self.mask_click_flag:
            self.mask_click_flag = False
            self.mask_all_point[str(len(self.mask_all_point) + 1)] = self.mask_now_point
            self.mask_now_point = []

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
            self.img_frame[0] = math.ceil(x - (x - self.img_frame[0]) * scale)
            self.img_frame[1] = math.ceil(y - (y - self.img_frame[1]) * scale)
            self.img_frame[2] = math.ceil(self.img_frame[2] * scale)
            self.img_frame[3] = math.ceil(self.img_frame[3] * scale)

        self.update()
        a0.accept()
