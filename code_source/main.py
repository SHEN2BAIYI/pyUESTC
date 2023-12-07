# 【main.py】
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QFont
from PyQt5.QtWidgets import *
import cv2

from XJ_Cropper import *
from XJ_TreeView import *
from XJ_LineEdit import *


class XJ_Main(QMainWindow):
    def __init__(self, parent=None):
        super(XJ_Main, self).__init__(parent)

        self.__canvas = XJ_Cropper()
        self.__files = XJ_TreeView()
        self.__path = XJ_LineEdit(self, '当前路径：', os.getcwd().replace('\\', '/') + '/', '选择目录')  # 路径名的反斜杠全改为斜杠
        self.__path.SetEnable_Input(False)
        self.__filesType = ['.png', '.jpg', '.bmp']  # 文件类型

        # 设置布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.__path)
        vbox.addWidget(self.__files)
        vbox.setStretchFactor(self.__files, 1)
        widget = QWidget()
        widget.setLayout(vbox)
        spt = QSplitter(Qt.Horizontal)
        spt.addWidget(widget)
        spt.addWidget(self.__canvas)
        self.setCentralWidget(spt)

        # 绑定响应函数
        self.__path.SetClicked_Button(self.__ClickPath)
        self.__files.doubleClicked.connect(self.__DoubleClickFiles)
        self.__canvas.btnClick_saveCrops.connect(self.__SaveCrops)

        # 其他的初始化
        self.__LoadDir()  # 初始化self.__files的内容

    def __ClickPath(self):  # 选择目录
        path = QFileDialog.getExistingDirectory(self, "选择目录").replace('\\', '/')  # 路径名的反斜杠全改为斜杠
        if (len(path)):
            path = path + '/'  # 加上一个斜杠
            self.__path.SetText_Input(path)
            self.__LoadDir()

    def __LoadPict(self, path):  # 加载路径下的图片
        cvImg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        qtImg = GetQPixmap(cvImg).toImage()
        self.__canvas.Load_Img(qtImg)
        self.__canvas.update()

    def __DoubleClickFiles(self, abc):  # 双击文件列表，如果是文件则更新裁剪图，如果是目录则更新目录。
        file = self.__files.GetCurrIter().GetData()[0]
        path = os.path.join(self.__path.GetText_Input(), file).replace('\\', '/')  # 路径名的反斜杠全改为斜杠

        if (os.path.isfile(path)):
            self.__LoadPict(path)
        else:
            if (file == '..'):  # 返回上一级目录
                path = self.__path.GetText_Input()
                path = path[:path[:-1].rfind('/') + 1]
            if (os.path.exists(path)):  # 以防万一的
                self.__path.SetText_Input(path)
                self.__LoadDir()

    def __LoadDir(self):  # 加载path下的文件及目录到XJ_TreeView中
        self.__files.Clear()
        iter = self.__files.GetHead()

        path = self.__path.GetText_Input()
        files = []
        folders = []
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                folders.append(f)
            elif self.__filesType.count(f[-4:]) != 0:
                files.append(f)

        font = QFont()
        font.setBold(True)
        font.setPixelSize(18)
        for f in files:
            iter.AppendRow([f]).SetFont(0, font)
        font.setBold(False)
        font.setItalic(True)
        font.setPixelSize(14)
        for f in folders:
            iter.AppendRow([f]).SetFont(0, font)
        if (path.count('/') > 1):
            iter.AppendRow(['..']).SetFont(0, font)  # 返回上一级目录

    def __SaveCrops(self):  # 导出图片
        crops = self.__canvas.Get_CropImgs()
        if (crops):
            path = QFileDialog.getExistingDirectory(self, "选择目录")
            if (path):
                file = self.__files.GetCurrIter().GetData()
                file = '空白图片.png' if file == None else file[0]
                file = file[:file.rfind('.')]
                path = os.path.join(path, file).replace('\\', '/')

                path_copy = path
                num = 1
                while (os.path.exists(path) and os.path.isdir(path)):
                    path = path_copy + '_' + str(num)
                    num = num + 1
                os.makedirs(path)

                for row in range(len(crops)):
                    for col in range(len(crops[row])):
                        file = os.path.join(path, '[{},{}].png'.format(row, col))
                        crops[row][col].save(file)
                QMessageBox.information(None, r'图片导出结束', '文件夹路径为：\n{}'.format(path))
        else:
            QMessageBox.information(None, r'失败', '截图不存在')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = XJ_Main()
    win.resize(1000, 500)
    win.show()
    win.setWindowTitle("XJ图片裁剪器")

    sys.exit(app.exec())
