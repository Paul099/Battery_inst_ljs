# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'read_adc_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(970, 461)
        Form.setStyleSheet("background-color: rgb(85, 0, 255);")
        self.show_read = QtWidgets.QLabel(Form)
        self.show_read.setGeometry(QtCore.QRect(10, 50, 950, 400))
        self.show_read.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.show_read.setText("")
        self.show_read.setObjectName("show_read")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(430, 10, 91, 31))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.show_label = QtWidgets.QLabel(Form)
        self.show_label.setGeometry(QtCore.QRect(520, 10, 111, 31))
        self.show_label.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.show_label.setText("")
        self.show_label.setAlignment(QtCore.Qt.AlignCenter)
        self.show_label.setObjectName("show_label")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(170, 85, 255);\n"
"color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.start_Button = QtWidgets.QPushButton(Form)
        self.start_Button.setGeometry(QtCore.QRect(680, 5, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.start_Button.setFont(font)
        self.start_Button.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.start_Button.setObjectName("start_Button")
        self.stop_Button = QtWidgets.QPushButton(Form)
        self.stop_Button.setGeometry(QtCore.QRect(800, 5, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.stop_Button.setFont(font)
        self.stop_Button.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.stop_Button.setObjectName("stop_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "测量值当前值: "))
        self.label_3.setText(_translate("Form", "测量值实时反馈折线图显示实验"))
        self.start_Button.setText(_translate("Form", "启动"))
        self.stop_Button.setText(_translate("Form", "停止"))

