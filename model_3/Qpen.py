#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example we draw 6 lines using
different pen styles. 

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
axis_x=[]
axis_y=[]
qpoints=[]
dic_qpoints=[]
max_y=0
class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Pen styles')
        self.read_points_draw_model()
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        print('paintevent')
        self.drawLines(qp)
        global dic_qpoints
        dic_qpoints=[]
        qp.end()
        
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        self.read_points_draw_model()
        print(dic_qpoints)
        for ch in dic_qpoints:
            for i in ch:
                i.setY(max_y-i.y())
        for ch in dic_qpoints:
            if ch:
                qp.drawPolygon(*ch)      
            else:
                break
        
    def find_max(self):
        #global maxnum
        global minimun
        maxnum=0
        minimum=0
        f=open('pde_gd.txt')
        while True:
            line=f.readline()
            if line:
                a=line.split('\t')
                inta=[float(i) for i in a]
                maxnum_line=max(inta[2:])
                minimum_line=min(inta[2:])
                if maxnum_line>maxnum:
                    maxnum=maxnum_line
                if minimum_line<minimum:
                    minimum=minimum_line
            else:
                break
        f.close()
        return maxnum,minimum
    def find_max_y(self):
        pass
    def read_points_draw_model(self):
        self.find_max()
        f=open('pde_gd.txt')
        while True:
            line=f.readline()
            if line:
                global axis_x
                global axis_y
                global max_y
                axis_x=[]
                axis_y=[]
                print(axis_x)
                a=line.split('\t')
                inta=[float(i) for i in a]
                num=int(inta[1])
                m=self.geometry()
                window_width=m.width()
                window_height=m.height()
                maxnum,minnum=self.find_max()
                inta=[(i+1.05*abs(minnum))/(maxnum-minnum) for i in inta]
                i=0;
                while i<num:
                    axis_x.append(inta[i+2])
                    axis_y.append(inta[i+2+num])
                    i=i+1
                axis_x=[0.9*i*window_width for i in axis_x]
                axis_y=[0.9*i*window_height for i in axis_y]
                max_y_find=max(axis_y)
                if max_y_find>max_y:
                    max_y=max_y_find
                point_num=len(axis_x)
                global dic_qpoints
                global qpoints
                qpoints=[]
                for i in range(0,point_num):
                    qpoint=QtCore.QPointF()
                    qpoint.setX(axis_x[i])
                    qpoint.setY(axis_y[i])
                    qpoints.append(qpoint)
                dic_qpoints.append(qpoints)
                print(dic_qpoints)
            else:
                break
        f.close()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
