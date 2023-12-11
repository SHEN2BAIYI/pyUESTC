# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageCropper.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1033, 870)
        self.imgFrame = QtWidgets.QFrame(Form)
        self.imgFrame.setGeometry(QtCore.QRect(10, 10, 671, 751))
        self.imgFrame.setStyleSheet("#imgFrame{border:1px solid rgb(123, 233, 255)}")
        self.imgFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgFrame.setObjectName("imgFrame")
        self.imgLabel = QtWidgets.QLabel(self.imgFrame)
        self.imgLabel.setGeometry(QtCore.QRect(10, 10, 651, 731))
        self.imgLabel.setObjectName("imgLabel")
        self.controlFrame = QtWidgets.QFrame(Form)
        self.controlFrame.setGeometry(QtCore.QRect(690, 10, 201, 751))
        self.controlFrame.setStyleSheet("#controlFrame{border:1px solid rgb(123, 233, 255)}")
        self.controlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlFrame.setObjectName("controlFrame")
        self.cropGroupBox = QtWidgets.QGroupBox(self.controlFrame)
        self.cropGroupBox.setGeometry(QtCore.QRect(10, 10, 181, 181))
        self.cropGroupBox.setObjectName("cropGroupBox")
        self.label = QtWidgets.QLabel(self.cropGroupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 131, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 151, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 151, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 151, 21))
        self.label_4.setObjectName("label_4")
        self.storeGroupBox = QtWidgets.QGroupBox(self.controlFrame)
        self.storeGroupBox.setGeometry(QtCore.QRect(10, 300, 181, 441))
        self.storeGroupBox.setObjectName("storeGroupBox")
        self.storeListView = QtWidgets.QListView(self.storeGroupBox)
        self.storeListView.setGeometry(QtCore.QRect(10, 130, 161, 231))
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
        self.storeButton.setGeometry(QtCore.QRect(10, 380, 161, 41))
        self.storeButton.setObjectName("storeButton")
        self.cropGroupBox_2 = QtWidgets.QGroupBox(self.controlFrame)
        self.cropGroupBox_2.setGeometry(QtCore.QRect(10, 200, 181, 91))
        self.cropGroupBox_2.setObjectName("cropGroupBox_2")
        self.checkBox = QtWidgets.QCheckBox(self.cropGroupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.checkBox.setChecked(True)
        self.checkBox.setTristate(True)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.imgLabel.setText(_translate("Form", "TextLabel"))
        self.cropGroupBox.setTitle(_translate("Form", "使用说明"))
        self.label.setText(_translate("Form", "鼠标左键进行勾画。"))
        self.label_2.setText(_translate("Form", "鼠标中键进行移动。"))
        self.label_3.setText(_translate("Form", "鼠标中键滚轮进行放大缩小。"))
        self.label_4.setText(_translate("Form", "鼠标右键双击取消勾画。"))
        self.storeGroupBox.setTitle(_translate("Form", "裁剪区域保存"))
        self.targetLabel_2.setText(_translate("Form", "保存文件夹："))
        self.storeLineEdit.setText(_translate("Form", "cropped"))
        self.targetLabel_3.setText(_translate("Form", "保存记录："))
        self.storeButton.setText(_translate("Form", "保存"))
        self.cropGroupBox_2.setTitle(_translate("Form", "附加操作"))
        self.checkBox.setText(_translate("Form", "保存裁剪信息"))
