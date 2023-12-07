# 【XJ_Cropper.py】
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QFont
from PyQt5.QtWidgets import *

from XJ_SampleCropper import *
from XJ_CropperSetting import XJ_SettingForCropper, XJ_SettingForMosaicBg


class XJ_Cropper(QWidget):  # 图片裁剪器（装入了按钮控件便于参数的设置
    btnClick_saveCrops = pyqtSignal()  # 当保存文件的按钮按下时发送信号

    def __init__(self, width=500, height=500, parent=None):
        super(XJ_Cropper, self).__init__(parent)
        self.resize(width, height)
        self.setFocusPolicy(Qt.ClickFocus | Qt.WheelFocus)  # 让控件可以获取焦点

        self.__cropper = XJ_SampleCropper(self)
        self.__setting_cropper = XJ_SettingForCropper(self)
        self.__setting_bg = XJ_SettingForMosaicBg(self)
        self.__text1 = QLabel('0x0', self)
        self.__text2 = QLabel('', self)
        self.__button = QPushButton('输出裁剪结果', self)

        # 设置布局
        vbox1 = QVBoxLayout()  # 装进裁剪器下方文本(__text1和__text2)
        vbox1.addWidget(self.__text1)
        vbox1.addWidget(self.__text2)
        hbox1 = QHBoxLayout()  # 装进裁剪器下方控件(按钮self.__button和文本vbox1)
        hbox1.addWidget(self.__button)
        hbox1.addStretch(1)
        hbox1.addLayout(vbox1)
        vbox1 = QVBoxLayout()  # 装进裁剪器以及裁剪器下方控件(裁剪器self.__cropper和下方控件hbox1)
        vbox1.addWidget(self.__cropper)
        vbox1.addLayout(hbox1)
        vbox2 = QVBoxLayout()  # 装进裁剪器右侧的裁剪设置(__setting_cropper和__setting_bg)
        vbox2.addWidget(self.__setting_cropper)
        vbox2.addWidget(self.__setting_bg)
        vbox2.addStretch(1)
        frame1 = QFrame()
        frame1.setLayout(vbox1)
        frame2 = QFrame()
        frame2.setLayout(vbox2)
        box = QHBoxLayout()
        box.addWidget(frame1)
        box.addWidget(frame2)
        self.setLayout(box)

        self.frame1 = frame1

        # 控制控件大小
        box.setStretchFactor(frame1, 1)
        vbox1.setStretchFactor(self.__cropper, 1)

        # 设置一些样式
        font = QFont()
        font.setBold(True)
        font.setPixelSize(24)
        self.__text1.setFont(font)
        self.__text1.setStyleSheet("QLabel{color:rgb(192,32,128);}")  # 设置颜色
        self.__text1.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # 设置居中靠右
        font.setPixelSize(20)
        self.__text2.setFont(font)
        self.__text2.setStyleSheet("QLabel{color:rgb(192,32,128);}")  # 设置颜色
        self.__text2.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # 设置居中靠右
        self.__button.setFont(font)
        self.__button.setStyleSheet(
            "QPushButton{border-radius:5px;border:2px solid rgb(192,32,128);color:rgb(192,32,128);} QPushButton:hover{border-color: green}")  # 设置颜色

        frame1.setObjectName('frame1')
        frame2.setObjectName('frame2')
        frame1.setStyleSheet(".QFrame#frame1{border-radius:10px;border:3px solid rgb(96,192,255)}")
        frame2.setStyleSheet(".QFrame#frame2{border-radius:10px;border:3px solid rgb(96,192,255)}")
        frame2.setFrameShape(QFrame.Box)  # 设置外边框

        # 绑定信号
        self.__setting_cropper.valueChange.connect(self.__SettingChange_Cropper)
        self.__setting_bg.valueChange.connect(self.__SettingChange_Bg)
        self.__cropper.valueChange.connect(self.__ValueChange_Cropper)
        self.__button.clicked.connect((lambda self: lambda: self.btnClick_saveCrops.emit())(self))

        # 更新设置
        self.__UpdateSetting()

    def Load_Img(self, Img):  # 设置图片
        self.__cropper.SetImg(Img)

    def Load_Setting(self, path):  # 加载配置
        pass

    def Save_Setting(self, path):  # 保存配置
        pass

    def Get_CropImgs(self):  # 获取裁剪结果
        return self.__cropper.Get_Crops()

    def __SettingChange_Cropper(self, val):  # 当关于裁剪器的设置发生变更时调用该函数
        cpr = self.__cropper
        setting = cpr.Get_Setting().cropper
        if (val[0] == '宽' or val[0] == '高'):
            val = self.__setting_cropper.Get_AspectRatio()
            cpr.Set_AspectRatio((val['宽'], val['高']))
        elif (val[0] == '行'):
            setting.rowCnt = val[1]
        elif (val[0] == '列'):
            setting.colCnt = val[1]
        elif (val[0] == '外线粗细'):
            setting.thickness_Border = val[1]
        elif (val[0] == '内线粗细'):
            setting.thickness_Inner = val[1]
        elif (val[0] == '外线颜色'):
            setting.color_Border = val[1]
        elif (val[0] == '内线颜色'):
            setting.color_Inner = val[1]
        elif (val[0] == '流畅裁剪'):
            cpr.Set_SmoothCrop(val[1])
        cpr.update()

    def __SettingChange_Bg(self, val):  # 当关于马赛克背景的设置发生变更时调用该函数
        cpr = self.__cropper
        setting = cpr.Get_Setting().bg
        if (val[0] == '颜色1'):
            setting.colors[0] = val[1]
        elif (val[0] == '颜色2'):
            setting.colors[1] = val[1]
        elif (val[0] == '格子大小'):
            setting.size = val[1]
        cpr.SetMosaicBg()

    def __ValueChange_Cropper(self):  # 当裁剪区发生变化时改变文本内容
        area = self.__cropper.Get_CropArea()
        if (area):
            area.Neaten()
            self.__text1.setText('{}x{}'.format(area.width, area.height))
            self.__text2.setText('{},{}'.format((area.left, area.top), (area.right - 1, area.bottom - 1)))
        else:
            self.__text1.setText('0x0')
            self.__text2.setText('')

    def __UpdateSetting(self):  # 更新裁剪器的设置
        cpr = self.__cropper
        cpr_setting = cpr.Get_Setting().cropper
        bg_setting = cpr.Get_Setting().bg
        setting_cpr = self.__setting_cropper
        setting_bg = self.__setting_bg

        cpr.Set_AspectRatio((setting_cpr.Get_AspectRatio()['宽'], setting_cpr.Get_AspectRatio()['高']))  # 裁剪的宽高比
        cpr.Set_SmoothCrop(setting_cpr.Get_SmoothCrop())  # 流畅裁剪
        cpr_setting.rowCnt = setting_cpr.Get_CntRowCol()['行']  # 行数
        cpr_setting.colCnt = setting_cpr.Get_CntRowCol()['列']  # 列数
        cpr_setting.thickness_Border = setting_cpr.Get_Thickness()['外线粗细']  # 外线粗细
        cpr_setting.thickness_Inner = setting_cpr.Get_Thickness()['内线粗细']  # 内线粗细
        cpr_setting.color_Border = setting_cpr.Get_BorderColor()['外线颜色']  # 外线颜色
        cpr_setting.color_Inner = setting_cpr.Get_BorderColor()['内线颜色']  # 内线颜色

        bg_setting.colors[0] = setting_bg.Get_Color1()
        bg_setting.colors[1] = setting_bg.Get_Color2()
        bg_setting.size = setting_bg.Get_Size()

        cpr.SetMosaicBg()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    cpr = XJ_Cropper(1200, 600)
    cpr.Load_Img(QImage('C:/Users/Administrator/Desktop/2.png'))
    cpr.btnClick_saveCrops.connect(lambda: print(cpr.Get_CropImgs()))
    cpr.show()

    sys.exit(app.exec())
