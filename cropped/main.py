from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from cropped.Cropper import Ui_MainWindow
from cropped.img_cropper import ImageCropper

import os
import sys
import cv2

class Cropper(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Cropper, self).__init__()
        self.setupUi(self)

        # 声明变量
        self.cwd = os.getcwd()
        self.store_list = []

        # 声明页面部件
        self.img_frame = ImageCropper()

        # 初始化
        self.__init_bind_event()
        self.__init_img_frame()
        self.__init_save_view()

    ########################
    #       初始化函数       #
    ########################
    """ 初始化主页面绑定事件 """
    def __init_bind_event(self):
        # 绑定文件夹选择事件
        self.targetLineEdit.mouseDoubleClickEvent = self.__choose_file
        # 绑定文件选择事件
        self.imgListView.doubleClicked.connect(self.__select_img_and_transfer)

        # 绑定微调按钮事件
        self.topUpButton.clicked.connect(lambda: self.__adjust_crop(1, -1))
        self.topDownButton.clicked.connect(lambda: self.__adjust_crop(1, 1))
        self.leftUpButton.clicked.connect(lambda: self.__adjust_crop(0, -1))
        self.leftDownButton.clicked.connect(lambda: self.__adjust_crop(0, 1))
        self.rightUpButton.clicked.connect(lambda: self.__adjust_crop(2, -1))
        self.rightDownButton.clicked.connect(lambda: self.__adjust_crop(2, 1))
        self.bottomUpButton.clicked.connect(lambda: self.__adjust_crop(3, -1))
        self.bottomDownButton.clicked.connect(lambda: self.__adjust_crop(3, 1))

        # 绑定保存按钮事件
        self.storeButton.clicked.connect(self.__save_crop)

    """ 初始化主页面图像操作区域 """
    def __init_img_frame(self):
        # 初始化图像编辑界面
        vbox = QVBoxLayout()
        vbox.addWidget(self.img_frame)
        self.imgFrame.setLayout(vbox)

    """ 初始化保存列表 """
    def __init_save_view(self):
        list_model = QStringListModel()
        list_model.setStringList(self.store_list)

        self.storeListView.setModel(list_model)
        self.storeListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    ########################
    #       功能性函数       #
    ########################
    """ 选择目录 """
    def __choose_file(self, is_dir=False, *args):
        if is_dir:
            file_name = QFileDialog.getExistingDirectory(self, "选取文件夹", self.cwd)
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "选取文件", self.cwd, 'Exe files(*.exe)')

        # 选择文件并传递给 line_edit
        if file_name:
            self.targetLineEdit.setText(file_name)

            # 读取文件夹下的文件
            files = os.listdir(file_name)
            files = [x for x in files if x.endswith('.jpg') or x.endswith('.png')]
            list_model = QStringListModel()
            list_model.setStringList(files)

            self.imgListView.setModel(list_model)
            self.imgListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    """ 选择图像文件，并进行传递 """
    def __select_img_and_transfer(self, item):
        # 获取文件名
        file_name = self.imgListView.selectionModel().selectedIndexes()[0].data()

        # 获取文件全路径
        file_path = os.path.join(self.targetLineEdit.text(), file_name)

        # 传递给图像编辑区域
        self.img_frame.reset()
        self.img_frame.set_img(file_path)

    """ 微调 crop 区域 """
    def __adjust_crop(self, target, step=1):
        # 获取当前 crop 区域
        crop = self.img_frame.crop_frame.copy()

        # 根据 target 选择 index。上(1)下(3)左(0)右(2)
        crop[target] += step

        self.img_frame.crop_frame = crop
        self.img_frame.update()

    """ 保存裁剪图像（并进行坐标同步） """
    def __save_crop(self):
        if not self.img_frame.crop_exits_flag:
            return

        # 将 crop 区域转换到原图像中
        img_frame = self.img_frame.img_frame.copy()
        crop_frame = self.img_frame.crop_frame.copy()
        # 加载原图像
        img = cv2.imread(self.img_frame.img_path)

        # 计算比例
        x1 = round((crop_frame[0] - img_frame[0]) * img.shape[1] / img_frame[2])
        y1 = round((crop_frame[1] - img_frame[1]) * img.shape[0] / img_frame[3])

        x2 = round((crop_frame[2] - img_frame[0]) * img.shape[1] / img_frame[2])
        y2 = round((crop_frame[3] - img_frame[1]) * img.shape[0] / img_frame[3])

        # 保存图像
        img = img[y1:y2, x1:x2]
        # 拆分图像路径
        file_path, file_name = os.path.split(self.img_frame.img_path)
        file_path = os.path.join(file_path, self.storeLineEdit.text())
        # 判断 file_path 文件夹是否存在
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, file_name)

        cv2.imwrite(file_path, img)
        # 显示保存记录
        if file_name not in self.store_list:
            self.store_list.append(file_name)
            self.__init_save_view()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Cropper()
    myWin.show()
    sys.exit(app.exec_())
