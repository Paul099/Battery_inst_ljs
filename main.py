from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QPalette
import dialog
import denglu
import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui
from dialog import Ui_Dialog
import datetime
from xianshi import Mygraphview


if __name__=='__main__':
   app = QApplication(sys.argv)
   form = QtWidgets.QWidget()
   window = Ui_Dialog()
   window.setupUi(form)
   form.show()
   sys.exit(app.exec_())



