# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Cropper.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1200, 800))
        self.centralwidget.setMaximumSize(QtCore.QSize(1200, 800))
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 281, 801))
        self.widget.setObjectName("widget")
        self.imgListView = QtWidgets.QListView(self.widget)
        self.imgListView.setGeometry(QtCore.QRect(10, 70, 261, 721))
        self.imgListView.setObjectName("imgListView")
        self.targetLabel = QtWidgets.QLabel(self.widget)
        self.targetLabel.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.targetLabel.setObjectName("targetLabel")
        self.targetLineEdit = QtWidgets.QLineEdit(self.widget)
        self.targetLineEdit.setGeometry(QtCore.QRect(80, 30, 191, 21))
        self.targetLineEdit.setReadOnly(True)
        self.targetLineEdit.setObjectName("targetLineEdit")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(280, 0, 921, 801))
        self.widget_2.setObjectName("widget_2")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setGeometry(QtCore.QRect(0, 0, 711, 801))
        self.widget_3.setObjectName("widget_3")
        self.imgFrame = QtWidgets.QFrame(self.widget_3)
        self.imgFrame.setGeometry(QtCore.QRect(0, 10, 701, 781))
        self.imgFrame.setStyleSheet("#imgFrame{border:1px solid rgb(123, 233, 255)}")
        self.imgFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgFrame.setObjectName("imgFrame")
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(710, 0, 211, 801))
        self.widget_4.setObjectName("widget_4")
        self.controlFrame = QtWidgets.QFrame(self.widget_4)
        self.controlFrame.setGeometry(QtCore.QRect(0, 10, 201, 781))
        self.controlFrame.setStyleSheet("#controlFrame{border:1px solid rgb(123, 233, 255)}")
        self.controlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlFrame.setObjectName("controlFrame")
        self.cropGroupBox = QtWidgets.QGroupBox(self.controlFrame)
        self.cropGroupBox.setGeometry(QtCore.QRect(10, 10, 181, 211))
        self.cropGroupBox.setObjectName("cropGroupBox")
        self.label = QtWidgets.QLabel(self.cropGroupBox)
        self.label.setGeometry(QtCore.QRect(30, 110, 16, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 16, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 16, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 16, 21))
        self.label_4.setObjectName("label_4")
        self.topDownButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.topDownButton.setGeometry(QtCore.QRect(110, 30, 21, 21))
        self.topDownButton.setObjectName("topDownButton")
        self.topUpButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.topUpButton.setGeometry(QtCore.QRect(70, 30, 21, 21))
        self.topUpButton.setObjectName("topUpButton")
        self.rightUpButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.rightUpButton.setGeometry(QtCore.QRect(70, 70, 21, 21))
        self.rightUpButton.setObjectName("rightUpButton")
        self.rightDownButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.rightDownButton.setGeometry(QtCore.QRect(110, 70, 21, 21))
        self.rightDownButton.setObjectName("rightDownButton")
        self.bottomUpButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.bottomUpButton.setGeometry(QtCore.QRect(70, 110, 21, 21))
        self.bottomUpButton.setObjectName("bottomUpButton")
        self.bottomDownButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.bottomDownButton.setGeometry(QtCore.QRect(110, 110, 21, 21))
        self.bottomDownButton.setObjectName("bottomDownButton")
        self.leftUpButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.leftUpButton.setGeometry(QtCore.QRect(70, 150, 21, 21))
        self.leftUpButton.setObjectName("leftUpButton")
        self.leftDownButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.leftDownButton.setGeometry(QtCore.QRect(110, 150, 21, 21))
        self.leftDownButton.setObjectName("leftDownButton")
        self.storeGroupBox = QtWidgets.QGroupBox(self.controlFrame)
        self.storeGroupBox.setGeometry(QtCore.QRect(10, 230, 181, 541))
        self.storeGroupBox.setObjectName("storeGroupBox")
        self.storeListView = QtWidgets.QListView(self.storeGroupBox)
        self.storeListView.setGeometry(QtCore.QRect(10, 130, 161, 321))
        self.storeListView.setObjectName("storeListView")
        self.targetLabel_2 = QtWidgets.QLabel(self.storeGroupBox)
        self.targetLabel_2.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.targetLabel_2.setObjectName("targetLabel_2")
        self.storeLineEdit = QtWidgets.QLineEdit(self.storeGroupBox)
        self.storeLineEdit.setGeometry(QtCore.QRect(10, 60, 161, 21))
        self.storeLineEdit.setReadOnly(True)
        self.storeLineEdit.setObjectName("storeLineEdit")
        self.targetLabel_3 = QtWidgets.QLabel(self.storeGroupBox)
        self.targetLabel_3.setGeometry(QtCore.QRect(10, 100, 91, 21))
        self.targetLabel_3.setObjectName("targetLabel_3")
        self.storeButton = QtWidgets.QPushButton(self.storeGroupBox)
        self.storeButton.setGeometry(QtCore.QRect(10, 480, 161, 41))
        self.storeButton.setObjectName("storeButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.targetLabel.setText(_translate("MainWindow", "目标文件夹："))
        self.cropGroupBox.setTitle(_translate("MainWindow", "裁剪框四边微调"))
        self.label.setText(_translate("MainWindow", "下"))
        self.label_2.setText(_translate("MainWindow", "上"))
        self.label_3.setText(_translate("MainWindow", "右"))
        self.label_4.setText(_translate("MainWindow", "左"))
        self.topDownButton.setText(_translate("MainWindow", "↓"))
        self.topUpButton.setText(_translate("MainWindow", "↑"))
        self.rightUpButton.setText(_translate("MainWindow", "←"))
        self.rightDownButton.setText(_translate("MainWindow", "→"))
        self.bottomUpButton.setText(_translate("MainWindow", "↑"))
        self.bottomDownButton.setText(_translate("MainWindow", "↓"))
        self.leftUpButton.setText(_translate("MainWindow", "←"))
        self.leftDownButton.setText(_translate("MainWindow", "→"))
        self.storeGroupBox.setTitle(_translate("MainWindow", "裁剪区域保存"))
        self.targetLabel_2.setText(_translate("MainWindow", "相对保存文件夹："))
        self.storeLineEdit.setText(_translate("MainWindow", "cropped"))
        self.targetLabel_3.setText(_translate("MainWindow", "保存记录："))
        self.storeButton.setText(_translate("MainWindow", "保存"))
