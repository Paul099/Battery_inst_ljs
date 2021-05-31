#!/usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time, random #导入时间模块和生成随机浮点数模块

from read_adc_ui import Ui_Form


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
            time.sleep(0.1)



class Show_adc(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Show_adc, self).__init__(parent)
        self.setupUi(self) #初始化ui

        self.init() #初始化变量
        self.signal_func() #信号槽链接函数

        if oneself == True:#如果是模块自己运行则启动多线程发送随机数
            self.thread = Show_Thread() #多线程实例化
            self.thread.start_timer() #启动线程
            self.thread.signal.connect(self.random_num) #线程启动槽函数

    #链接信号槽函数
    def signal_func(self):
        self.start_Button.clicked.connect(self.start_func) #启动按钮单击信号
        self.stop_Button.clicked.connect(self.stop_func)  #停止按钮单击信号

    #生成随机数
    def random_num(self):
        num = random.uniform(0, 5) # 生成随机数，浮点类型
        num1 = round(num, 2) # 控制随机数的精度，保留两位小数
        self.count_dot(num1)

    #初始化变量函数
    def init(self):
        self.draw = QPainter()  # 绘制类实例
        self.picture = QPixmap(950,400) #设置图片大小
        self.end_dot_list = [ [0, 0] ] #保存绘制点位列表
        self.x_num = 100 #X轴分成多少等份
        self.y_num = 5 #Y轴分成多少等份

        self.x_num1 = 950/self.x_num #每一等份的宽度
        self.y_num1 = 400/self.y_num #每一等份的高度

        self.run_signal = False #运行标志位

    #启动按钮槽函数，置位运行标志
    def start_func(self):
        self.run_signal = True

    #停止按钮槽函数，复位运行标志
    def stop_func(self):
        self.run_signal = False

    #修改列表点位
    def count_dot(self, value):
        if self.run_signal == True:
            self.show_label.setText(str(value)) #设置标签显示当前值
            self.beg_x = 0    #初始化起点
            self.beg_y = 400  #初始化起点
            if len(self.end_dot_list) >= (self.x_num+1): #X轴950化成95等份
                self.end_dot_list = self.end_dot_list[-self.x_num: ] #截取列表保留后95位
                for i in self.end_dot_list: #遍历列表，每个点位X轴左移一位(即减小1)
                    i[0] -= self.x_num1
            x = self.end_dot_list[-1][0] + self.x_num1 #新增点位的X轴
            y = value                        #新增点位的Y轴
            self.end_dot_list.append([x, y]) #将新增的点位添加到列表

            self.picture.fill(Qt.white)  # 设置为白底色
            self.read_dot()  # 读取列表点位进行绘制

    #读取列表点位进行绘制
    def read_dot(self):
        #解析列表中点位进行移位计算
        for end_dot_list in self.end_dot_list:
            self.end_x = end_dot_list[0]        # X轴终点位置
            # 输入的数值为0-5.画布高度为400，画布左上角为0，0。改为左下角为0，0
            self.end_y = 400 - end_dot_list[1] * self.y_num1
            self.uptate_show() #调用绘制图形

        self.show_read.setPixmap(self.picture) # 将图像显示在标签上

    #绘制函数
    def uptate_show(self):
        self.draw.begin(self.picture) # 开始在目标设备上面绘制
        self.draw.setPen(QPen(QColor("black"), 1))# 设置画笔颜色，粗细
        # 绘制一条指定了端点坐标的线，绘制从（self.beg_x,self.beg_y）到（self.end_x,self.end_y）的直线
        self.draw.drawLine(QPoint(self.beg_x, self.beg_y),QPoint(self.end_x, self.end_y) )
        self.draw.end() #结束在目标设备上面绘制
        self.beg_x = self.end_x #改变结束后的坐标
        self.beg_y = self.end_y



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    oneself = True #标志为模块自己运行
    main = Show_adc( )
    main.show()
    sys.exit(app.exec_())
