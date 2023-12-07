# 【XJ_LineEdit.py】
import sys
from PyQt5.QtWidgets import *


class XJ_LineEdit(QWidget):
    def __init__(self, parent=None, hint='提示文本：', input='内容文本', button='按钮文本'):
        super(XJ_LineEdit, self).__init__(parent)
        self.__hint = QLabel(hint, self)
        self.__input = QLineEdit(input, self)
        self.__button = QPushButton(button, self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.__hint)
        hbox.addWidget(self.__input)
        hbox.addWidget(self.__button)
        self.setLayout(hbox)

    def SetText_Hint(self, tx):
        self.__hint.setText(tx)

    def SetText_Button(self, tx):
        self.__button.setText(tx)

    def GetText_Input(self):
        return self.__input.text()

    def SetText_Input(self, tx):
        self.__input.setText(tx)

    def SetClicked_Button(self, func):
        self.__button.clicked.connect(func)

    def SetEnable_Input(self, flag):
        self.__input.setReadOnly(not flag)

    def SetEnable_Button(self, flag):
        self.__button.setVisible(flag)

    def GetWidget_Hint(self):
        return self.__hint

    def GetWidget_Input(self):
        return self.__input

    def GetWidget_Button(self):
        return self.__button


if __name__ == '__main__':
    app = QApplication(sys.argv)

    le = XJ_LineEdit()
    le.show()

    sys.exit(app.exec())

