# 【XJ_NumInput.py】
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class XJ_NumInput(QLineEdit):
    valueChange = pyqtSignal(int)  # 槽信号，值修改时发送信号

    def __init__(self, valMin=0, valMax=100, parent=None):
        super(XJ_NumInput, self).__init__(str(valMin), parent)
        self.__curr = valMin  # __curr是用来判断当前值有无发生修改的

        font = QFont()
        font.setBold(True)
        font.setPixelSize(20)

        self.setMouseTracking(True)  # 时刻捕捉鼠标移动
        self.setReadOnly(True)  # 设置只读
        self.setFont(font)  # 设置字体
        self.setAlignment(Qt.AlignCenter)  # 设置居中
        self.setMaximumWidth(80)

        self.Set_ValueRange(valMin, valMax)

    def focusOutEvent(self, event):  # 脱离焦点
        self.__LimitValue()
        self.setReadOnly(True)
        event.accept()

    def mouseMoveEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)  # 手型光标
        event.accept()

    def mouseDoubleClickEvent(self, event):
        self.setReadOnly(False)
        self.setFocus()
        event.accept()

    def wheelEvent(self, event):
        delta = event.angleDelta()
        curr = int(self.text())
        if (delta.y() > 0):  # 滚轮向上滚动，增加
            if (curr < self.__val_max):
                curr = curr + 1
        elif (delta.y() < 0):  # 向下滚动，减少
            if (curr > self.__val_min):
                curr = curr - 1
        self.setText(str(curr))
        self.update()
        event.accept()

        if (curr != self.__curr):
            self.__curr = curr
            self.valueChange.emit(curr)

    def Set_ValueRange(self, valMin, valMax):
        self.__val_min = valMin
        self.__val_max = valMax
        if (self.__val_max < self.__val_min):
            self.__val_max, self.__val_min = self.__val_min, self.__val_max
        self.__LimitValue()

    def Get_ValueRange(self):  # 返回取值范围
        return (self.__val_min, self.__val_max)

    def Set_Value(self, val):
        self.setText(str(val))
        self.__LimitValue()

    def Get_Value(self):
        return int(self.text())

    def __LimitValue(self):
        curr = ''.join(list(filter(lambda c: c.isdigit() or c == '+' or c == '-', self.text()))).lstrip('0')
        curr = int(eval(curr)) if len(curr) else 0
        if (curr < self.__val_min):
            curr = self.__val_min
        if (curr > self.__val_max):
            curr = self.__val_max
        self.setText(str(curr))

        if (curr != self.__curr):
            self.__curr = curr
            self.valueChange.emit(curr)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tmp = XJ_NumInput()
    tmp.show()

    tmp.valueChange.connect(lambda i: print(i))

    sys.exit(app.exec())

