# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImBalancer.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1022, 859)
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
        self.cropGroupBox.setGeometry(QtCore.QRect(10, 10, 181, 251))
        self.cropGroupBox.setObjectName("cropGroupBox")
        self.label_2 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 51, 21))
        self.label_2.setObjectName("label_2")
        self.rangeSlider = QtWidgets.QSlider(self.cropGroupBox)
        self.rangeSlider.setGeometry(QtCore.QRect(30, 60, 141, 16))
        self.rangeSlider.setMinimum(20)
        self.rangeSlider.setMaximum(60)
        self.rangeSlider.setSingleStep(2)
        self.rangeSlider.setProperty("value", 20)
        self.rangeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.rangeSlider.setObjectName("rangeSlider")
        self.label_3 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 170, 51, 21))
        self.label_3.setObjectName("label_3")
        self.withdrawButton = QtWidgets.QPushButton(self.cropGroupBox)
        self.withdrawButton.setGeometry(QtCore.QRect(30, 200, 141, 23))
        self.withdrawButton.setObjectName("withdrawButton")
        self.degreeSlider = QtWidgets.QSlider(self.cropGroupBox)
        self.degreeSlider.setGeometry(QtCore.QRect(30, 130, 141, 16))
        self.degreeSlider.setMinimum(1)
        self.degreeSlider.setMaximum(10)
        self.degreeSlider.setSingleStep(1)
        self.degreeSlider.setProperty("value", 1)
        self.degreeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.degreeSlider.setObjectName("degreeSlider")
        self.label_4 = QtWidgets.QLabel(self.cropGroupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 100, 51, 21))
        self.label_4.setObjectName("label_4")
        self.storeGroupBox = QtWidgets.QGroupBox(self.controlFrame)
        self.storeGroupBox.setGeometry(QtCore.QRect(10, 270, 181, 471))
        self.storeGroupBox.setObjectName("storeGroupBox")
        self.storeListView = QtWidgets.QListView(self.storeGroupBox)
        self.storeListView.setGeometry(QtCore.QRect(10, 150, 161, 201))
        self.storeListView.setObjectName("storeListView")
        self.targetLabel_2 = QtWidgets.QLabel(self.storeGroupBox)
        self.targetLabel_2.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.targetLabel_2.setObjectName("targetLabel_2")
        self.storeLineEdit = QtWidgets.QLineEdit(self.storeGroupBox)
        self.storeLineEdit.setGeometry(QtCore.QRect(10, 90, 161, 21))
        self.storeLineEdit.setReadOnly(True)
        self.storeLineEdit.setObjectName("storeLineEdit")
        self.targetLabel_3 = QtWidgets.QLabel(self.storeGroupBox)
        self.targetLabel_3.setGeometry(QtCore.QRect(10, 120, 91, 21))
        self.targetLabel_3.setObjectName("targetLabel_3")
        self.storeButton = QtWidgets.QPushButton(self.storeGroupBox)
        self.storeButton.setGeometry(QtCore.QRect(10, 410, 161, 41))
        self.storeButton.setObjectName("storeButton")
        self.testButton = QtWidgets.QPushButton(self.storeGroupBox)
        self.testButton.setGeometry(QtCore.QRect(10, 360, 161, 41))
        self.testButton.setObjectName("testButton")
        self.allCheckBox = QtWidgets.QCheckBox(self.storeGroupBox)
        self.allCheckBox.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.allCheckBox.setObjectName("allCheckBox")
        self.paramCheckBox = QtWidgets.QCheckBox(self.storeGroupBox)
        self.paramCheckBox.setGeometry(QtCore.QRect(90, 30, 71, 16))
        self.paramCheckBox.setObjectName("paramCheckBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.imgLabel.setText(_translate("Form", "TextLabel"))
        self.cropGroupBox.setTitle(_translate("Form", "设置"))
        self.label_2.setText(_translate("Form", "影响范围"))
        self.label_3.setText(_translate("Form", "撤销按钮"))
        self.withdrawButton.setText(_translate("Form", "撤销"))
        self.label_4.setText(_translate("Form", "影响程度"))
        self.storeGroupBox.setTitle(_translate("Form", "保存"))
        self.targetLabel_2.setText(_translate("Form", "保存文件夹："))
        self.storeLineEdit.setText(_translate("Form", "imBalanced"))
        self.targetLabel_3.setText(_translate("Form", "保存记录："))
        self.storeButton.setText(_translate("Form", "保存"))
        self.testButton.setText(_translate("Form", "测试"))
        self.allCheckBox.setText(_translate("Form", "重复操作"))
        self.paramCheckBox.setText(_translate("Form", "参数保存"))
