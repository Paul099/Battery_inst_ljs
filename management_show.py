'''
2020.05.21
脚本用于继承power_management.ui的界面，实现功能
'''
import csv
import sys
import serial
import time
import numpy as np
import matplotlib
import threading
matplotlib.use("Qt5Agg")  # 声明使用QT5

from datetime import datetime
import pyqtgraph as pg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui,QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import jiemiang
import Login
import settings

#STRGLO=[0X01,]*26 #读取的数据
BOOL=True  #读取标志位



class MyWidget(QtWidgets.QMainWindow,jiemiang.Ui_Form):
    '''主界面'''
    def __init__(self,parent=None):
        super(MyWidget,self).__init__(parent)
        self.setupUi(self)
        self.inputPowerButton1.clicked.connect(self.inputPower_set_max_current)
        self.outputButton1.clicked.connect(self.outputPower_start_shiebei1)#设备一放电
        self.my_login= MyLogin()

    def add_sum(self,a):
        sum = 0
        for i in a:
            sum = sum + i
        sum =  sum & 0x000000FF
        return sum


    def inputPower_set_max_current(self,):
        '''设定输入电流值'''
        current = 1#暂时写死数据
        #后面用服务器返回的数据来取代设定的大小
        cmd = [0x00, ] * 26
        # cmd=[0xaa,0x00,1,1,1,1,1,1]
        cmd[0] = 0xaa
        int_current = np.int32(current * 1000)
        cmd[2] = 0x2a
        cmd[3] = int_current & 0x000000FF
        cmd[4] = (int_current & 0x0000FF00) >> 8
        cmd[5] = (int_current & 0x00FF0000) >> 16
        cmd[6] = (int_current & 0xFF000000) >> 24

        cmd[25] = self.add_sum(cmd)
        print('inputPower_set_current:cmd[25]',cmd[25])
        # self.ser = serial.Serial("COM5", 9600, timeout=5)
        # self.ser.write(cmd)
        #self.my_login.ser.write(cmd)
        mylogin.ser.write(cmd)



    def outputPower_start_shiebei1(self):
        '''设备1放电'''
        if mylogin.ser.is_open:
            print('串口5打开！')
        current = 12#暂时写死数据
        int_current = np.int32(current * 1000)
        #后面用服务器返回的数据来取代设定的大小
        cmd = [0x00, ] * 26
        # cmd=[0xaa,0x00,1,1,1,1,1,1]
        cmd[0] = 0xaa
        cmd[2] = 0x5F#43H读取负载相应的单步电压值
        # cmd[3] = 0x0a #00 0a 两个字节，表示00 10 mv单步步进电压值（量程精度）
        # cmd[4] = 0x00
        # cmd[5] = int_current & 0x000000FF     #设定的电压或者读取值
        # cmd[6] = (int_current & 0x0000FF00) >> 8
        # cmd[7] = (int_current & 0x00FF0000) >> 16
        # cmd[8] = (int_current & 0xFF000000) >> 24
        # cmd[9] = 0x96#00004096设定的1000ms电压值
        # cmd[10] = 0x40

        cmd[25] = self.add_sum(cmd)
        mylogin.ser.write(cmd)
        time.sleep(2)
        # sum = 0
        # for i in range(3,8):
        #     sum =sum +mylogin.STRGLO[i]
        #
        #np.int32(sum)
        vol_sum = []
        vol_sum.append(mylogin.STRGLO[3] & 0x000000FF)
        vol_sum.append((mylogin.STRGLO[4] & 0x000000FF) << 8)
        vol_sum.append((mylogin.STRGLO[5] & 0x000000FF) << 16)
        vol_sum.append((mylogin.STRGLO[6] & 0x000000FF) << 24)
        sum =0
        for i in vol_sum:
            sum=i +sum


        self.outputVoltageEdit1.setText(str(sum))
        print('sum:',sum)





class MyLogin(QtWidgets.QMainWindow,Login.Ui_Form):
    '''登录界面'''
    def __init__(self,parent=None):
        super(MyLogin,self).__init__(parent)
        self.setupUi(self)
        self.returnMsg.setText('')
        self.pushButtonLogin.clicked.connect(self.login)#信号槽函数
        self.closecontrolButton.clicked.connect(self.close_control)



    def login(self):
        '''登录'''
        username = self.userNameEdit.text()
        #psw = int(self.passwordEdit.text())#关闭验证

        if username=='root' or username!='root':
            self.returnMsg.setText('登录成功！')
            #self.hide()
            serial_state = self.serial_setting()
            if serial_state:
                self.returnMsg.setText('登录成功！串口连接成功！')
                self.ser.write([0xAA,0x00,0x20,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xCB])
                #p1=threading.Thread(target=mylogin.ReadData)#读串口进程


            else:
                self.returnMsg.setText('登录成功！串口连接失败！')
            time.sleep(1)
            self.my_widget = MyWidget()
            self.my_widget.show()
            self.my_login = MyLogin()
            self.my_login.close()
            p1 = threading.Thread(target=mylogin.ReadData)
            p1.start()
        else:
            self.returnMsg.setText('用户名或密码错误，登录失败！')


    def close_control(self):
        '''电子负载断开槽函数'''
        self.ser.write(
            [0xAA, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xCA])
        self.returnMsg.setText('电子负载自动测试断开！')
        mylogin.ser.close()
        print("串口关闭！")

    def serial_setting(self):
        '''连接串口指令'''
        try:
            # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
            portx = "COM5"
            # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
            bps = 9600
            # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
            timex = 5
            # 打开串口，并得到串口对象
            self.ser = serial.Serial(portx, bps, timeout=timex)
            return self.ser.is_open
            # fp = 0
            # while True:
            #     fp = fp + 1
            #     str = input('输入：')
            #     # 写数据
            #     result = ser.write(str.encode("gbk"))
            #     print("写总字节数:", result)
            #     if fp > 5:
            #         break
            #ser.close()  # 关闭串口

        except Exception as e:
            print("---异常---：", e)


    def ReadData(self):
        #global STRGLO, BOOL
        # 循环接收数据，此为死循环，可用线程实现
        while BOOL:
            if self.ser.in_waiting:#self.ser.in_waiting:
                #msg = self.ser.readall()
                #self.msg_list = list(msg.hex)
                self.STRGLO = self.ser.read(self.ser.in_waiting)
                print('STRGLO:',self.STRGLO)
                #print(self.msg_list)
                #print('STRGLO[5],STRGLO[6],STRGLO[7],STRGLO[8]:',STRGLO[5],STRGLO[6],STRGLO[7],STRGLO[8])





class MySettings(QtWidgets.QMainWindow,settings.Ui_Form):
    '''设置界面'''
    def __init__(self,parent=None):
        super(MySettings,self).__init__(parent)
        self.setupUi(self)


class Figure_Canvas(FigureCanvas):
    # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height),
                     dpi=dpi)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111)  # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法

    def test(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)


# 创建一个GraphicsView实例化显示
class Mygraphview(jiemiang.Ui_Form, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Mygraphview, self).__init__(parent)
        self.setupUi(self)
        self.paint_plot()

    # 将波形嵌入QGraph_view控件
    def paint_plot(self):
        Graphview = Figure_Canvas()
        Graphview.test()
        # 创建一个QGraphicsScene，因为加载的图形（FigureCanvas）
        # 不能直接放到graphicview控件中，必须先放到graphicScene
        # 然后再把graphicscene放到graphicview中
        graphicscene = QtWidgets.QGraphicsScene()
        # 把图形放到QGraphicsScene中
        # 注意：图形是作为一个QWidget放到QGraphicsScene中的
        graphicscene.addWidget(Graphview)
        self.graphicsStateUI.setScene(graphicscene)  # 把QGraphicsScene放入QGraphicsView
        self.graphicsStateUI.show()  # 调用show方法呈现图形！Voila!!

# class My_appwindow(SerialInit,Mygraphview):
# 示波器上位机显示
#    def __init__(self):
#        super().__init__()
#        self.paint_plot()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mylogin =MyLogin()
    mylogin.show()

    # mygraph = Mygraphview()
    # mygraph.show()
    app.exec_()
    #sys.exit(app.exec_())
