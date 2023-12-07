# 【XJ_ColorChoose.py】
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *


class XJ_ColorChoose(QLabel):  # 小控件，点击弹出换色窗口。QWidget子类化时样式表不生效，np
    valueChange = pyqtSignal(tuple)  # 槽信号，值修改时发送信号

    def __init__(self, rgb=(255, 50, 50), width=10, parent=None):
        super(XJ_ColorChoose, self).__init__(parent)
        self.setMouseTracking(True)  # 时刻捕捉鼠标移动
        self.__color = QColor(*rgb)
        self.__SetColor()
        self.SetWidth(width)

    def __SetColor(self):
        self.setStyleSheet("QLabel{{background-color:rgb{0};}};".format(self.Get_Color()))  # 设置颜色
        self.update()

    def mouseMoveEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)  # 手型光标

    def mousePressEvent(self, event):  # 设置点击事件
        if event.button() == Qt.LeftButton:  # 左键点击
            col = QColorDialog.getColor()
            if (col.isValid()):
                self.__color = col
                self.__SetColor()
                self.valueChange.emit(self.Get_Color())  # 值修改时发送信号

    def SetWidth(self, width):
        s = ' ' * width
        self.setText(s)

    def Get_Color(self):
        col = self.__color
        return (col.red(), col.green(), col.blue())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    test = XJ_ColorChoose()
    test.show()

    test.valueChange.connect(lambda t: print(t))

    sys.exit(app.exec())

