from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui.image_cropper import ImageCropper
from ui.flaw_remover import FlawRemover
from ui.basic import MainWindow

import os
import sys
import cv2


class WIM(QMainWindow, MainWindow):
    def __init__(self):
        super(WIM, self).__init__()
        self.setupUi(self)
        self.setMouseTracking(True)
        self.cwd = os.getcwd()

        # 裁剪页面部件
        self.cropper = ImageCropper()
        vbox = QStackedLayout()
        vbox.addWidget(self.cropper)
        self.cropTab.setLayout(vbox)

        # 缺陷修复页面部件
        self.flaw_remover = FlawRemover()
        vbox = QStackedLayout()
        vbox.addWidget(self.flaw_remover)
        self.flawRemoveTab.setLayout(vbox)

        # 初始化
        self.__init_bind_event()

    """ 初始化主页面绑定事件 """
    def __init_bind_event(self):
        # 绑定文件夹选择事件
        self.targetLineEdit.mouseDoubleClickEvent = self.__choose_file
        # 绑定文件选择事件
        self.imgListView.doubleClicked.connect(self.__select_img_and_transfer)

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

        # 判断当前 tab 页面，进行传递
        if self.tabWidget.currentIndex() == 1:
            self.flaw_remover.reset()
            self.flaw_remover.set_img(file_path)
        elif self.tabWidget.currentIndex() == 0:
            self.cropper.reset()
            self.cropper.set_img(file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WIM()
    window.show()
    sys.exit(app.exec_())
