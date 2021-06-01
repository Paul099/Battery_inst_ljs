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
import random
matplotlib.use("Qt5Agg")  # 声明使用QT5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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
        self.my_login = MyLogin()
        #self.my_widget = MyWidget()
        self.inputPowerButton1.clicked.connect(self.inputPower_set_max_current)
        self.outputButton1.clicked.connect(self.outputPower_start_shiebei1)#设备一放电
        self.vol_current = 0
        self.update_para = threading.Thread(target=self.timer_para)


        self.init()  # 初始化变量
        self.pushButton_3.clicked.connect(self.start_func)  # 启动按钮单击信号

        if oneself == True:  # 如果是模块自己运行则启动多线程发送随机数
            self.thread = Show_Thread()  # 多线程实例化
            self.thread.start_timer()  # 启动线程
            self.thread.signal.connect(self.random_num)  # 线程启动槽函数

    # 将波形嵌入QGraph_view控件

    # 生成随机数
    def random_num(self):


        #num = random.uniform(0, 5)  # 生成随机数，浮点类型
        num1 = round(self.vol_current, 4)  # 控制随机数的精度，保留两位小数#修改成显示的电压值
        self.count_dot(num1)
        #print('count_dot(num1)',num1)

        # 初始化变量函数

    def init(self):
        self.draw = QPainter()  # 绘制类实例
        self.picture = QPixmap(330, 330)  # 设置图片大小
        self.end_dot_list = [[0, 0]]  # 保存绘制点位列表
        self.x_num = 200  # X轴分成多少等份
        self.y_num = 10  # Y轴分成多少等份

        self.x_num1 = 330 / self.x_num  # 每一等份的宽度
        self.y_num1 = 330 / self.y_num  # 每一等份的高度

        self.run_signal = False  # 运行标志位

        # 启动按钮槽函数，置位运行标志

    def start_func(self):
        self.run_signal = True

        # 停止按钮槽函数，复位运行标志

    def stop_func(self):
        self.run_signal = False

        # 修改列表点位

    def count_dot(self, value):
        if self.run_signal == True:
            # self.show_label.setText(str(value))  # 设置标签显示当前值
            self.beg_x = 0  # 初始化起点
            self.beg_y = 330  # 初始化起点
            if len(self.end_dot_list) >= (self.x_num + 1):  # X轴950化成95等份
                self.end_dot_list = self.end_dot_list[-self.x_num:]  # 截取列表保留后95位
                for i in self.end_dot_list:  # 遍历列表，每个点位X轴左移一位(即减小1)
                    i[0] -= self.x_num1
            x = self.end_dot_list[-1][0] + self.x_num1  # 新增点位的X轴
            y = value  # 新增点位的Y轴
            self.end_dot_list.append([x, y])  # 将新增的点位添加到列表

            self.picture.fill(Qt.white)  # 设置为白底色
            self.read_dot()  # 读取列表点位进行绘制
        # 读取列表点位进行绘制

    def read_dot(self):
        # 解析列表中点位进行移位计算
        for end_dot_list in self.end_dot_list:
            self.end_x = end_dot_list[0]  # X轴终点位置
            # 输入的数值为0-5.画布高度为400，画布左上角为0，0。改为左下角为0，0
            self.end_y = 330 - end_dot_list[1] * self.y_num1
            self.uptate_show()  # 调用绘制图形

        self.show_curve.setPixmap(self.picture)  # 将图像显示在标签上

    def uptate_show(self):
        self.draw.begin(self.picture)  # 开始在目标设备上面绘制
        self.draw.setPen(QPen(QColor("black"), 1))  # 设置画笔颜色，粗细
        # 绘制一条指定了端点坐标的线，绘制从（self.beg_x,self.beg_y）到（self.end_x,self.end_y）的直线
        self.draw.drawLine(QPoint(self.beg_x, self.beg_y), QPoint(self.end_x, self.end_y))
        self.draw.end()  # 结束在目标设备上面绘制
        self.beg_x = self.end_x  # 改变结束后的坐标
        self.beg_y = self.end_y


    def add_sum(self,a):
        sum = 0
        for i in a:
            sum = sum + i
        sum =  sum & 0x000000FF
        return sum


    def add_sum_para_show(self,para):
        '''计算四个字节的参数和'''
        sum = 0
        for i in para:
            sum = sum + i
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
            print('串口5打开！开始放电显示')

        cmd = [0x00, ] * 26
        cmd[0] = 0xaa
        cmd[2] = 0x5F#43H读取负载相应的单步电压值
        cmd[25] = self.add_sum(cmd)
        mylogin.ser.write(cmd)
        time.sleep(2)#等待串口返回数据

        '''定时器显示刷新'''
        # timer = threading.Timer(1,self.timer_para)
        # timer.start()
        # timer = QtCore.QTimer()
        # #timer.timeout.connect(lambda :MyWidget.timer_para(self))
        # timer.timeout.connect(self.timer_para)#同上面的方法都可实现定时器的定时
        # timer.start(250)
        #print('timer',type(timer))
        '''将返回的串口数据4-7字节返回'''
        vol_sum = []
        self.vol_record = []#存储数据
        vol_sum.append(mylogin.STRGLO[3] & 0x000000FF)
        vol_sum.append((mylogin.STRGLO[4] & 0x000000FF) << 8)
        vol_sum.append((mylogin.STRGLO[5] & 0x000000FF) << 16)
        vol_sum.append((mylogin.STRGLO[6] & 0x000000FF) << 24)
        self.vol_current = self.add_sum_para_show(vol_sum)/1000#显示电压值
        print('self.vol_current',self.vol_current)
        self.vol_record.append(self.vol_current)#存储的电压值

        cur_sum = []
        self.cur_record = []#存储数据
        cur_sum.append(mylogin.STRGLO[7] & 0x000000FF)
        cur_sum.append((mylogin.STRGLO[8] & 0x000000FF) << 8)
        cur_sum.append((mylogin.STRGLO[9] & 0x000000FF) << 16)
        cur_sum.append((mylogin.STRGLO[10] & 0x000000FF) << 24)
        self.cur_current = self.add_sum_para_show(cur_sum)/10000#显示电压值单位是0.1mv
        print('self.cur_current', self.cur_current)
        self.vol_record.append(self.cur_current)#存储的电流值


        self.outputVoltageEdit1.setText(str(self.vol_current))#显示电压
        self.outputCurrentEdit1.setText(str(self.cur_current))#显示电流
        self.outputEndVoltageEdit1.setText(str(10.00))#暂时写死从数据库读取
        self.update_para.start()





    def timer_para(self):
        '''刷新数据'''
        '''将返回的串口数据4-7字节返回'''
        while True:

            time.sleep(0.25)
            cmd = [0x00, ] * 26
            cmd[0] = 0xaa
            cmd[2] = 0x5F#43H读取负载相应的单步电压值
            cmd[25] = self.add_sum(cmd)
            mylogin.ser.write(cmd)

            vol_sum = []
            self.vol_record = []#存储数据
            vol_sum.append(mylogin.STRGLO[3] & 0x000000FF)
            vol_sum.append((mylogin.STRGLO[4] & 0x000000FF) << 8)
            vol_sum.append((mylogin.STRGLO[5] & 0x000000FF) << 16)
            vol_sum.append((mylogin.STRGLO[6] & 0x000000FF) << 24)
            self.vol_current = self.add_sum_para_show(vol_sum)/1000#显示电压值
            #print('self.vol_current',self.vol_current)
            self.vol_record.append(self.vol_current)#存储的电压值

            cur_sum = []
            self.cur_record = []#存储数据
            cur_sum.append(mylogin.STRGLO[7] & 0x000000FF)
            cur_sum.append((mylogin.STRGLO[8] & 0x000000FF) << 8)
            cur_sum.append((mylogin.STRGLO[9] & 0x000000FF) << 16)
            cur_sum.append((mylogin.STRGLO[10] & 0x000000FF) << 24)
            self.cur_current = self.add_sum_para_show(cur_sum)/1000#显示电压值
            #print('self.cur_current', self.cur_current)
            self.vol_record.append(self.cur_current)#存储的电流值

            self.outputVoltageEdit1.setText(str(self.vol_current))#显示电压
            self.outputCurrentEdit1.setText(str(self.cur_current))#显示电流
            # print('self.vol_current',self.vol_current)
            # print('self.cur_current', self.cur_current)
            # print('定时器开启')



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
            #time.sleep(1)
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



#Qt多线程，
class Show_Thread(QThread):
    signal = pyqtSignal() #信号

    def __init__(self,parent=None):
        super(Show_Thread,self).__init__(parent)

    def start_timer(self):
       self.start() #启动线程

    def run(self):
        while True:
            self.signal.emit() #发送信号
            time.sleep(1)#发射信号的时间



class Show_adc(QtWidgets.QMainWindow,Login.Ui_Form):
    def __init__(self, parent=None):
        super(Show_adc, self).__init__(parent)
        self.setupUi(self) #初始化ui






class MySettings(QtWidgets.QMainWindow,settings.Ui_Form):
    '''设置界面'''
    def __init__(self,parent=None):
        super(MySettings,self).__init__(parent)
        self.setupUi(self)


class Figure_Canvas(FigureCanvas):
    # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height),
                     dpi=dpi)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)

        #self.axes = fig.add_subplot(111)  # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法


# 创建一个GraphicsView实例化显示
class Mygraphview(QtWidgets.QMainWindow, jiemiang.Ui_Form):
    def __init__(self, parent=None):
        super(Mygraphview, self).__init__(parent)
        self.setupUi(self)




    # def paint_plot(self):
    #     Graphview = Figure_Canvas()
    #     Graphview.test()
    #     # 创建一个QGraphicsScene，因为加载的图形（FigureCanvas）
    #     # 不能直接放到graphicview控件中，必须先放到graphicScene
    #     # 然后再把graphicscene放到graphicview中
    #     graphicscene = QtWidgets.QGraphicsScene()
    #     # 把图形放到QGraphicsScene中
    #     # 注意：图形是作为一个QWidget放到QGraphicsScene中的
    #     graphicscene.addWidget(Graphview)
    #     self.F3_view_11.setScene(graphicscene)  # 把QGraphicsScene放入QGraphicsView
    #     self.F3_view_11.show()  # 调用show方法呈现图形！Voila!!


class My_appwindow(MyWidget,Mygraphview):
    def __init__(self, parent = None):
        super(My_appwindow,self).__init__(parent)
        self.paint_plot()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    oneself = True  # 标志为模块自己运行
    mylogin =MyLogin()
    mylogin.show()

    # mygraph = Mygraphview()
    # mygraph.show()
    app.exec_()
    #sys.exit(app.exec_())
