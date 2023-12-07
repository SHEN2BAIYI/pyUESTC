# 【XJ_CropperSetting.py】
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import *

from XJ_NumInput import *
from XJ_ColorChoose import *


class XJ_ColorWithHint(QWidget):  # 带有Hint的XJ_ColorChoose
    def __init__(self, hint, hintFont, color, horizontal=True, parent=None):
        super(XJ_ColorWithHint, self).__init__(parent)
        self.hint = QLabel(hint, self)
        self.color = XJ_ColorChoose(color, 10, self)

        self.hint.setFont(hintFont)  # 设置字体
        self.hint.setAlignment(Qt.AlignCenter)  # 设置居中
        box = QHBoxLayout() if horizontal else QVBoxLayout()
        box.addWidget(self.hint)
        box.addWidget(self.color)
        self.setLayout(box)


class XJ_NumWithHint(QWidget):  # 带有Hint的XJ_NumInput
    def __init__(self, hint, hintFont, valMin, valMax, horizontal=True, parent=None):
        super(XJ_NumWithHint, self).__init__(parent)
        self.hint = QLabel(hint, self)
        self.num = XJ_NumInput(valMin, valMax, self)
        self.hint.setFont(hintFont)  # 设置字体
        self.hint.setAlignment(Qt.AlignCenter)  # 设置居中

        box = QHBoxLayout() if horizontal else QVBoxLayout()
        box.addWidget(self.hint)
        box.addWidget(self.num)
        self.setLayout(box)


class XJ_SettingForCropper(QWidget):  # 与图片裁剪相关的设置
    valueChange = pyqtSignal(tuple)  # 值发生改变时发射信号，值为二元组

    # 信号内容取值如下：
    # ('宽'：int)
    # ('高'：int)
    # ('行'：int)
    # ('列'：int)
    # ('外线粗细'：int)
    # ('内线粗细'：int)
    # ('外线颜色'：(int,int,int))
    # ('内线颜色'：(int,int,int))
    # ('流畅裁剪'：bool)
    def __init__(self, parent=None):
        super(XJ_SettingForCropper, self).__init__(parent)
        self.setFocusPolicy(Qt.ClickFocus | Qt.WheelFocus)  # 让控件可以获取焦点

        # 生成控件
        font = QFont()
        font.setBold(True)
        font.setPixelSize(16)
        self.__aspectRatio = [XJ_NumWithHint('宽', font, 0, 100, True), XJ_NumWithHint('高', font, 0, 100, True)]  # 长宽比
        self.__cntRowCol = [XJ_NumWithHint('行数', font, 1, 100, True),
                            XJ_NumWithHint('列数', font, 1, 100, True)]  # 分割数
        self.__thickness = [XJ_NumWithHint('外线', font, 1, 5, True), XJ_NumWithHint('内线', font, 1, 5, True)]  # 边界粗细
        self.__borderColor = [XJ_ColorWithHint('外线', font, (255, 50, 50), self),
                              XJ_ColorWithHint('内线', font, (64, 0, 255), self)]  # 边界颜色
        self.__smoothCrop = [QCheckBox(self)]  # 流畅裁剪

        # 设置布局
        box = QVBoxLayout()
        lst = [
            [QLabel('宽高比', self), self.__aspectRatio],
            [QLabel('分割数', self), self.__cntRowCol],
            [QLabel('边界粗细', self), self.__thickness],
            [QLabel('边界颜色', self), self.__borderColor],
            [QLabel('流畅裁剪', self), self.__smoothCrop]
        ]
        for pst in range(len(lst)):
            hint = lst[pst][0]
            hint.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # 设置居中靠右
            hint.setFont(font)
            hint.setStyleSheet("QLabel{color:rgb(192,64,64);}")  # 设置颜色

            box1 = QVBoxLayout()  # 竖直盒子
            for wid in lst[pst][1]:
                box1.addWidget(wid)
            box2 = QHBoxLayout()  # 水平盒子
            box2.addWidget(hint)
            box2.addStretch(1)
            box2.addLayout(box1)
            frame = QFrame()
            frame.setLayout(box2)
            frame.setFrameShape(QFrame.StyledPanel)  # 设置外边框
            box.addWidget(frame)
        self.setLayout(box)

        # 绑定信号
        def SetFunc(self, key):  # 整个闭包，省的翻车
            def Func(val):
                self.valueChange.emit((key, val))

            return Func

        self.__aspectRatio[0].num.valueChange.connect(SetFunc(self, '宽'))
        self.__aspectRatio[1].num.valueChange.connect(SetFunc(self, '高'))
        self.__cntRowCol[0].num.valueChange.connect(SetFunc(self, '行'))
        self.__cntRowCol[1].num.valueChange.connect(SetFunc(self, '列'))
        self.__thickness[0].num.valueChange.connect(SetFunc(self, '外线粗细'))
        self.__thickness[1].num.valueChange.connect(SetFunc(self, '内线粗细'))
        self.__borderColor[0].color.valueChange.connect(SetFunc(self, '外线颜色'))
        self.__borderColor[1].color.valueChange.connect(SetFunc(self, '内线颜色'))

        def SetFunc(self):  # 整个闭包，省的翻车
            def Func():
                self.valueChange.emit(('流畅裁剪', self.__smoothCrop[0].isChecked()))

            return Func

        self.__smoothCrop[0].clicked.connect(SetFunc(self))

        self.__thickness[0].num.Set_Value(4)
        self.__thickness[1].num.Set_Value(2)
        self.__cntRowCol[0].num.Set_Value(3)
        self.__cntRowCol[1].num.Set_Value(3)

    def Get_AspectRatio(self):
        nums = self.__aspectRatio
        return {'宽': nums[0].num.Get_Value(), '高': nums[1].num.Get_Value()}

    def Get_CntRowCol(self):
        nums = self.__cntRowCol
        return {'行': nums[0].num.Get_Value(), '列': nums[1].num.Get_Value()}

    def Get_Thickness(self):
        nums = self.__thickness
        return {'外线粗细': nums[0].num.Get_Value(), '内线粗细': nums[1].num.Get_Value()}

    def Get_BorderColor(self):
        cols = self.__borderColor
        return {'外线颜色': cols[0].color.Get_Color(), '内线颜色': cols[1].color.Get_Color()}

    def Get_SmoothCrop(self):
        return self.__smoothCrop[0].isChecked()


class XJ_SettingForMosaicBg(QWidget):  # 与马赛克背景相关的设置
    valueChange = pyqtSignal(tuple)  # 值发生改变时发射信号，值为二元组

    # 信号内容取值如下：
    # ('颜色1',(int,int,int))
    # ('颜色2',(int,int,int))
    # ('格子大小',int)
    def __init__(self, parent=None):
        super(XJ_SettingForMosaicBg, self).__init__(parent)
        self.setFocusPolicy(Qt.ClickFocus | Qt.WheelFocus)  # 让控件可以获取焦点

        # 生成控件
        font = QFont()
        font.setBold(True)
        font.setPixelSize(16)
        self.__color1 = XJ_ColorWithHint('颜色1', font, (255, 255, 255))
        self.__color2 = XJ_ColorWithHint('颜色2', font, (192, 228, 228))
        self.__size = XJ_NumWithHint('格子大小', font, 1, 1024)
        hint = QLabel('马赛克背景', self)
        hint.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # 设置居中靠右
        hint.setFont(font)
        hint.setStyleSheet("QLabel{color:rgb(192,64,64);}")  # 设置颜色

        # 设置布局
        box1 = QVBoxLayout()
        box1.addWidget(self.__color1)
        box1.addWidget(self.__color2)
        box1.addWidget(self.__size)
        box2 = QHBoxLayout()
        box2.addWidget(hint)
        box2.addStretch(1)
        box2.addLayout(box1)
        box = QVBoxLayout()
        frame = QFrame()
        frame.setLayout(box2)
        frame.setFrameShape(QFrame.StyledPanel)  # 设置外边框
        box.addWidget(frame)
        self.setLayout(box)

        self.__size.num.Set_Value(16)

        # 绑定信号
        def SetFunc(self, key):  # 整个闭包，省的翻车
            def Func(val):
                self.valueChange.emit((key, val))

            return Func

        self.__color1.color.valueChange.connect(SetFunc(self, '颜色1'))
        self.__color2.color.valueChange.connect(SetFunc(self, '颜色2'))
        self.__size.num.valueChange.connect(SetFunc(self, '格子大小'))

    def Get_Color1(self):
        return self.__color1.color.Get_Color()

    def Get_Color2(self):
        return self.__color2.color.Get_Color()

    def Get_Size(self):
        return self.__size.num.Get_Value()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    set1 = XJ_SettingForCropper()
    set1.show()

    set2 = XJ_SettingForMosaicBg()
    set2.show()

    set1.valueChange.connect(lambda val: print(val))
    set2.valueChange.connect(lambda val: print(val))

    sys.exit(app.exec())

