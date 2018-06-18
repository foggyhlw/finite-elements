#!/usr/bin/python3
# -*- coding: utf-8 -*-
import constants
import fem
import calculate_gap_B
import calculate_B
import sys, random
import solveEquation
import calculate_B_lines
from RawData import RawData
import os
import numpy as np
from scipy.interpolate import griddata
from PyQt4 import QtGui,QtCore
import matplotlib.pyplot as pl
what_to_paint=''
highlight_num=0
ModelColor=QtCore.Qt.black
LineColor=QtCore.Qt.green
ModelPen=2
LinePen=1
PATH='model_2'
total_highlight_line=set() 
class Paint(QtGui.QWidget):
    def __init__(self):
        super(Paint, self).__init__()
        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Pen styles')
        self.show()

    def paintEvent(self, e):
        #global PATH
        qp = QtGui.QPainter()
        qp.begin(self)
        global what_to_paint
        if what_to_paint == 'model':
            dic_qpoints=self.read_points_draw_model()
            self.drawModel(qp,dic_qpoints)
        if what_to_paint=='split':
            split_points,split_triangles=self.read_points_Split('%s/pde_p.txt'%PATH,'%s/pde_t.txt'%PATH)
            self.drawSplit(qp,split_points,split_triangles)
            dic_qpoints=self.read_points_draw_model()
            self.drawModel(qp,dic_qpoints)
        if what_to_paint=='refined_split':
            split_points,split_triangles=self.read_points_Split('%s/pde_refine_p.txt'%PATH,'%s/pde_refine_t.txt'%PATH)
            self.drawSplit(qp,split_points,split_triangles)
            dic_qpoints=self.read_points_draw_model()
            self.drawModel(qp,dic_qpoints)
        if what_to_paint=='B_lines':
            blines_points=self.read_points_Blines()
            self.draw_Blines(qp,blines_points)
            dic_qpoints=self.read_points_draw_model()
            self.drawModel(qp,dic_qpoints)
        if what_to_paint=='highlight_line':
            dic_qpoints=self.read_points_draw_model()
            self.drawModel(qp,dic_qpoints)
            num=list(total_highlight_line)
            for i in num:
                highlight_points=self.read_points_highlight(i)
                self.draw_highlight_line(qp,highlight_points,LineColor)
      #  if what_to_paint=='highlight_line_cancel':
      #      dic_qpoints=self.read_points_draw_model()
      #      self.drawModel(qp,dic_qpoints)
      #      highlight_points=self.read_points_highlight(highlight_num)
      #      self.draw_highlight_line(qp,highlight_points,ModelColor)
        qp.end()
        
    def drawModel(self, qp, dic_qpoints):#画模型
        pen = QtGui.QPen(ModelColor, ModelPen)
        qp.setPen(pen)
        for ch in dic_qpoints:
            for i in ch:
                window_width,window_height=self.find_geometry_size()
                i.setY(window_height-i.y())
        for ch in dic_qpoints:
            if ch:
                qp.drawPolygon(*ch)      
            else:
                break

    def drawSplit(self,qp,split_points,split_triangles):#画剖分
        pen = QtGui.QPen(LineColor, LinePen)
        qp.setPen(pen)
        for p in split_triangles:
            p1=split_points[p[0]-1]
            p2=split_points[p[1]-1]
            p3=split_points[p[2]-1]
            qp.drawPolygon(p1,p2,p3)

    def draw_Blines(self,qp,blines_points):#画磁力线
        pen = QtGui.QPen(LineColor, LinePen, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for ch in blines_points:
            if ch:
                qp.drawLine(*ch)      
            else:
                break

    def draw_highlight_line(self,qp,highlight_points,Color):
        pen=QtGui.QPen(Color,ModelPen,QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(*highlight_points)

    def find_max_min(self,address):#找到数据点中xy最大最小值，用来计算相对坐标值
        maxnum_x=0
        minnum_x=0
        maxnum_y=0
        minnum_y=0
        f=open(address)
        while True:
            line=f.readline()
            if line:
                a=line.split('\t')
                inta=[float(i) for i in a]
                if inta[0]>maxnum_x:
                    maxnum_x=inta[0]
                if inta[0]<minnum_x:
                    minnum_x=inta[0]
                if inta[1]>maxnum_y:
                    maxnum_y=inta[1]
                if inta[1]<minnum_y:
                    minnum_y=inta[1]
            else:
                break
        f.close()
        return maxnum_x,minnum_x,maxnum_y,minnum_y

    def find_geometry_size(self):#找到当然画布大小（以像素为单位）
        m=self.geometry()
        window_width=m.width()-1 #防止画图出界
        window_height=m.height()-1
        return window_width,window_height

    def read_points_draw_model(self):#读取模型点数据，以x1，x2... y1,y2形式读取，存为QPintF点列表，每个区域存为一个列表
        f=open("%s/pde_gd.txt"%PATH)
        dic_qpoints=[]
        while True:
            line=f.readline()
            if line:
                axis_x=[]
                axis_y=[]
                a=line.split('\t')
                inta=[float(i) for i in a]
                num=int(inta[1])
                maxnum_x,minnum_x,maxnum_y,minnum_y=self.find_max_min('%s/pde_p.txt'%PATH)
                window_width,window_height=self.find_geometry_size()
                #inta=[(i-minnum)/(maxnum-minnum) for i in inta]
                i=0;
                while i<num:
                    axis_x.append(inta[i+2])
                    axis_y.append(inta[i+2+num])
                    i=i+1
                axis_x=[(m-minnum_x)*window_width/(maxnum_x-minnum_x) for m in axis_x]
                axis_y=[(m-minnum_y)*(window_height)/(maxnum_y-minnum_y) for m in axis_y]
                point_num=len(axis_x)
                qpoints=[]
                for i in range(0,point_num):
                    qpoint=QtCore.QPointF()
                    qpoint.setX(axis_x[i])
                    qpoint.setY(axis_y[i])
                    qpoints.append(qpoint)
                dic_qpoints.append(qpoints)
            else:
                break
        f.close()
        return dic_qpoints

    def read_points_Split(self,file_p,file_t):
        f_points=open(file_p)
        f_triangles=open(file_t)
        points=[]
        triangles=[]
        Qtpoints=[]
        for a in f_points:
            a=a.split('\t')
            b=[float(i) for i in a]
            points.append(b)
        maxnum_x,minnum_x,maxnum_y,minnum_y=self.find_max_min('%s/pde_p.txt'%PATH)#这里由于数据格式问题，使用模型中的最大最小值，而非剖分文件中的值
        window_width,window_height=self.find_geometry_size()
        for a in points:
            Qtpoint=QtCore.QPointF()
            Qtpoint.setX((a[0]-minnum_x)*(window_width-1)/(maxnum_x-minnum_x))
            Qtpoint.setY((window_height-(a[1]-minnum_y)*(window_height)/(maxnum_y-minnum_y)))
            Qtpoints.append(Qtpoint)
        for a in f_triangles:
            a=a.split('\t')
            b=[int(i) for i in a]
            triangles.append(b)
        f_points.close()
        f_triangles.close()
        return Qtpoints,triangles

    def read_points_Blines(self):
        f=open('%s/B_lines_file.txt'%PATH)
        maxnum_x,minnum_x,maxnum_y,minnum_y=self.find_max_min('%s/pde_p.txt'%PATH)#这里由于数据格式问题，使用模型中的最大最小值，而非剖分文件中的值
        window_width,window_height=self.find_geometry_size()
        Qtpoints=[]
        for a in f:
            a=a.split('\t')
            b=[float(i) for i in a]
            point_num=len(b)
            for i in range(0,point_num,4):
                qpoints=[]
                for m in range(0,2):
                    qpoint=QtCore.QPointF()
                    qpoint.setX((b[i+2*m]-minnum_x)*window_width/(maxnum_x-minnum_x))
                    qpoint.setY((window_height-(b[i+1+2*m]-minnum_y)*window_height/(maxnum_y-minnum_y)))
                    qpoints.append(qpoint)
                Qtpoints.append(qpoints)
        f.close()
        return Qtpoints

    def read_points_highlight(self,num):
        maxnum_x,minnum_x,maxnum_y,minnum_y=self.find_max_min('%s/pde_p.txt'%PATH)
        window_width,window_height=self.find_geometry_size()
        points=[]
        point_file=RawData('%s/pde_g.txt'%PATH)
        point_file.load()
        for i in range(1,3):
            Qpoint=QtCore.QPointF()
            Qpoint.setX(((point_file[num-1][i])-minnum_x)*window_width/(maxnum_x-minnum_x))
            Qpoint.setY(window_height-((point_file[num-1][i+2])-minnum_y)*window_height/(maxnum_y-minnum_y))
            points.append(Qpoint)
        return points
    
class Newwindow(QtGui.QWidget):
    def __init__(self):
        super(Newwindow,self).__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('gap')
        self.show()

class Mainwindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.initUI()
        
    def initUI(self):               
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        openAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open file')
        openAction.triggered.connect(self.fileopen_triggered)

        modelAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&ShowModel', self)        
        modelAction.triggered.connect(self.model_triggered)
        boundaryAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&ShowBoundary', self)        
        boundaryAction.triggered.connect(self.boundary_triggered)
        meshAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Mesh', self)        
        meshAction.triggered.connect(self.mesh_triggered)
        refinedmeshAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Refinedmesh', self)        
        refinedmeshAction.triggered.connect(self.refinedmesh_triggered)
        makeMatrixAction=QtGui.QAction(QtGui.QIcon(''),'&MakeMatrix',self)
        makeMatrixAction.triggered.connect(self.makematrix_triggered)
        solverconfigureAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Configure', self)        
        solverconfigureAction.triggered.connect(self.solverconfigure_triggered)
        solveAction = QtGui.QAction(QtGui.QIcon('./pixmaps/16.gif'), '&Solve', self)        
        solveAction.setStatusTip('please wait while solving matrix...')
        solveAction.triggered.connect(self.solve_triggered)
        calgapBAction=QtGui.QAction(QtGui.QIcon(''),'&CalgapB',self)
        calgapBAction.triggered.connect(self.calgapB_triggered)
        bmapAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit.png'),'&Map of B',self)
        bmapAction.triggered.connect(self.bmap_triggered)
        cloudAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit.png'),'&Cloud map',self)
        cloudAction.triggered.connect(self.cloud_triggered)
        gapAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit.png'),'&Gap B',self)
        gapAction.triggered.connect(self.gap_triggered)

        self.statusBar()

        menu_file = self.menuBar()
        fileMenu = menu_file.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        fileMenu = menu_file.addMenu("&Model")
        fileMenu.addAction(modelAction)
        fileMenu = menu_file.addMenu("&Boundary")
        fileMenu.addAction(boundaryAction)
        fileMenu = menu_file.addMenu("&Mesh")
        fileMenu.addAction(meshAction)
        fileMenu.addAction(refinedmeshAction)
        fileMenu = menu_file.addMenu("&Solver")
        fileMenu.addAction(solverconfigureAction)
        fileMenu.addAction(makeMatrixAction)
        fileMenu.addAction(solveAction)
        fileMenu.addAction(calgapBAction)
        fileMenu = menu_file.addMenu("&Postprocess")
        fileMenu.addAction(bmapAction)
        fileMenu.addAction(cloudAction)
        fileMenu.addAction(gapAction)
        
        saveAction=QtGui.QAction(QtGui.QIcon('pngs/floppy-drive.png'),'Save',self)
        saveAction.setShortcut('Ctrl+O')
#        saveAction.triggered.connect(self.Save_Image)
        colorAction=QtGui.QAction(QtGui.QIcon('pngs/colorboard.png'),'Color',self)
        colorAction.triggered.connect(self.Color_Choose)
        penAction=QtGui.QAction(QtGui.QIcon('pngs/pen.png'),'Pen',self)
        penAction.triggered.connect(self.Pen_Choose)
        
        self.toolbar=self.addToolBar('Configure')
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(colorAction)
        self.toolbar.addAction(penAction)

        self.drawingwindow=QtGui.QWidget()
        self.drawingwindow.setStyleSheet("QWidget {background-color:'White'}")
        self.drawingwindow_layout=QtGui.QHBoxLayout()
        self.modelmap=Paint()
        self.drawingwindow_layout.addWidget(self.modelmap)

        grid_layout=QtGui.QGridLayout()
        grid_layout.addLayout(self.drawingwindow_layout,0,0,2,1)
        self.drawingwindow.setLayout(grid_layout)

        self.setCentralWidget(self.drawingwindow)
        
        self.setGeometry(200,100,800,600)
        self.setWindowTitle('Finite elements')    
        self.show()

    def find_max_min(self,address):#找到数据点中xy最大最小值，用来计算相对坐标值
        maxnum_x=0
        minnum_x=0
        maxnum_y=0
        minnum_y=0
        f=open(address)
        while True:
            line=f.readline()
            if line:
                a=line.split('\t')
                inta=[float(i) for i in a]
                if inta[0]>maxnum_x:
                    maxnum_x=inta[0]
                if inta[0]<minnum_x:
                    minnum_x=inta[0]
                if inta[1]>maxnum_y:
                    maxnum_y=inta[1]
                if inta[1]<minnum_y:
                    minnum_y=inta[1]
            else:
                break
        f.close()
        return maxnum_x,minnum_x,maxnum_y,minnum_y

    def read_points_cloudmap(self,file_p,file_t,file_m):
        f_points=open(file_p)
        f_triangles=open(file_t)
        f_magnitude=open(file_m)
        points_centrol=[]
        triangles=[]
        Qtpoints=[]
        B_magnitude=[]
        points=[]
        for a in f_points:
            a=a.split('\t')
            b=[float(i) for i in a]
            points.append(b)
        maxnum_x,minnum_x,maxnum_y,minnum_y=self.find_max_min('%s/pde_p.txt'%PATH)#这里由于数据格式问题，使用模型中的最大最小值，而非剖分文件中的值
        for a in points:
            Qtpoints.append([(a[0]-minnum_x),(a[1-minnum_y])])
        for a in f_triangles:
            a=a.split('\t')
            b=[int(i) for i in a]
            triangles.append(b)
        for a in f_magnitude:
            a=a.split('\t')
            B_magnitude.append(a[2])
        for a in triangles:
            x_average=(Qtpoints[a[0]-1][0]+Qtpoints[a[1]-1][0]+Qtpoints[a[2]-1][0])/3/(maxnum_x-minnum_x)
            y_average=(Qtpoints[a[0]-1][1]+Qtpoints[a[1]-1][1]+Qtpoints[a[2]-1][1])/3/(maxnum_y-minnum_y)
            points_centrol.append([x_average,y_average])
        f_magnitude.close()
        f_points.close()
        f_triangles.close()
        print(len(points_centrol),len(B_magnitude))
        return points_centrol,B_magnitude


    def draw_Cloudmap(self,points_centrol,B_magnitude):
        grid_x,grid_y=np.mgrid[0:1:800j,0:1:600j]
        grid=griddata(points_centrol,B_magnitude,(grid_x,grid_y),method='linear')
        pl.imshow(grid.T, aspect='auto', extent=(0,1,0,1), origin='lower',interpolation='bilinear')
        pl.title('Cloud_map')
        pl.colorbar()
        pl.jet()
        pl.show()

    def fileopen_triggered(self):
        global file_name
        file_name=QtGui.QFileDialog.getOpenFileName(self,'Open file','/home')
        print(file_name)        
    def model_triggered(self):
        global what_to_paint
        what_to_paint='model'
        self.modelmap.update()
    def boundary_triggered(self):
        self.boundary_window=boundary_Window(self)
    def mesh_triggered(self):
        global what_to_paint
        what_to_paint='split'
        self.modelmap.update()
    def refinedmesh_triggered(self):
        global what_to_paint
        what_to_paint='refined_split'
        self.modelmap.update()
        pass
    def makematrix_triggered(self):
        import makeEquation
        makeEquation.main()
        self.statusBar().showMessage('makematrix done!')
    def solverconfigure_triggered(self):
        self.onfigure_window=Configure_Window()
    def solve_triggered(self):
        self.message_wait()
        solveEquation.main()
        self.statusBar().showMessage('done!')
    def calgapB_triggered(self):
        calculate_B.main()
        calculate_gap_B.main()
        self.statusBar().showMessage('Gap_B calculating done!')
    def bmap_triggered(self):
        calculate_B_lines.main()
        global what_to_paint
        what_to_paint='B_lines'
        self.modelmap.update()
    def cloud_triggered(self):
        import showCloud
        points_centrol,B_magnitude=self.read_points_cloudmap('%s/pde_refine_p.txt'%PATH,'%s/pde_refine_t.txt'%PATH,'%s/B_file.txt'%PATH)
        self.draw_Cloudmap(points_centrol,B_magnitude)
    def gap_triggered(self):
        f=open('%s/gapB_file.txt'%PATH)
        axis_x=[]
        axis_y=[]
        for points in f:
            points=points.split('\t')
            points=[float(a) for a in points]
            axis_x.append(points[0])
            axis_y.append(points[1])
        pl.plot(axis_x,axis_y)
        pl.xlabel('location')
        pl.ylabel('T')
        pl.title('Gap_B')
        pl.show()
    def message_wait(self):
        self.statusBar().showMessage('calculating...')
    def Color_Choose(self):
        self.col=colorBoard()
    def Pen_Choose(self):
        self.PenBoard=PenBox()

class boundary_Window(QtGui.QWidget):

    def __init__(self,parent):
        super(boundary_Window,self).__init__()
        self.initUI(self)
        self.parent=parent
    def initUI(self,parent):
        f=open('%s/pde_g.txt'%PATH)
        a=f.readlines()
        self.boundary_num=len(a)
        self.Window=QtGui.QWidget()
        self.combolist=[]
        line_check_list=[]
        self.values=[]
        boundary_default=RawData('%s/boundary_parameter.txt'%PATH)
        if boundary_default.empty()!=1:
            boundary_default.load()
        print(boundary_default)
        self.lbl_boun_num=QtGui.QLabel('Boundary Num')
        self.lbl_boun_style=QtGui.QLabel('Boundary Style')
        self.lbl_boun_value=QtGui.QLabel('Value')
        grid_layout=QtGui.QGridLayout()
        for i in range(0,self.boundary_num):
            self.lbl_nums=QtGui.QLabel('Line %d'%(i+1))
            grid_layout.addWidget(self.lbl_nums,i,0)
            self.style_choose=QtGui.QComboBox(self)
            self.style_choose.setMinimumHeight(20)
            self.style_choose.addItem('0')
            self.style_choose.addItem('1')
            self.style_choose.addItem('2')
            self.combolist.append(self.style_choose)
            #self.style_choose.setItemText(boundary_default[i][0],'%d'%boundary_default[i][0])
            grid_layout.addWidget(self.style_choose,i,2)
            self.line_check=QtGui.QCheckBox('%d'%(i+1))
            self.line_check.stateChanged.connect(self.hightlight_line)
            #self.line_check.toggle()
            line_check_list.append(self.line_check)
            grid_layout.addWidget(self.line_check,i,1)
            self.value_input=QtGui.QLineEdit('',self)
            self.value_input.setMaximumWidth(40)
            self.value_input.setMinimumHeight(20)
            if boundary_default[i][0]!=0:
                self.value_input.setText('%d'%boundary_default[i][1])
            self.values.append(self.value_input.text())
            grid_layout.addWidget(self.value_input,i,3)
            self.style_choose.setCurrentIndex(boundary_default[i][0])
        self.button_ok=QtGui.QPushButton('OK',self)
        self.button_ok.setMaximumWidth(80)
        self.button_ok.clicked.connect(self.parameter_load)
        self.button_cancel=QtGui.QPushButton('cancel',self)
        self.button_cancel.setMaximumWidth(80)
        self.button_cancel.clicked.connect(self.close)
        grid_layout.addWidget(self.button_ok,self.boundary_num+1,1)
        grid_layout.addWidget(self.button_cancel,self.boundary_num+1,2,1,2)

        self.scrollarea=QtGui.QScrollArea()
        self.Window.setLayout(grid_layout)
        self.Window.setGeometry(300,300,300,800)
        #self.setTittle('Boundary Conditions')
        self.scrollarea.setWidget(self.Window)
        Window_layout=QtGui.QVBoxLayout()
        Window_layout.addWidget(self.scrollarea)
        self.setLayout(Window_layout)
        self.show()
        f.close()
    def parameter_load(self):
        boundary_to_change=RawData('%s/boundary_parameter.txt'%PATH)
        for i in range(0,self.boundary_num):
            if self.combolist[i].currentText()!=0:
                boundary_to_change.append([self.combolist[i].currentText(),self.values[i]])
            else:
                boundary_to_change.append([self.combolist[i].currentText(),])
        boundary_to_change.save()
        self.close()
    def hightlight_line(self,state):
        global what_to_paint
        global highlight_num
        global total_highlight_line
        highlight_lines=RawData('%s/pde_g.txt'%PATH)
        sender=self.sender()
        line_num=sender.text()
        if state==QtCore.Qt.Checked:
            what_to_paint='highlight_line'
            highlight_num=int(sender.text())
            total_highlight_line.add(highlight_num)
            self.parent.modelmap.update()
        else:
            what_to_paint='highlight_line'
            highlight_num=int(sender.text())
            total_highlight_line.discard(highlight_num)
            self.parent.modelmap.update()


class colorBoard(QtGui.QWidget):
    def __init__(self):
        super(colorBoard,self).__init__()
        self.initUI()

    def initUI(self):
        self.button_ok=QtGui.QPushButton('OK!',self)
        self.button_ok.clicked.connect(self.apply_color)
        self.button_ok.setMaximumWidth(60)
        self.button_default=QtGui.QPushButton('Cancel',self)
        self.button_default.clicked.connect(self.cancel)
        self.button_default.setMaximumWidth(60)
        self.lbl_modelcolor=QtGui.QLabel('ModelColor')
        self.lbl_linecolor=QtGui.QLabel('LineColor')
        self.button_model_color=QtGui.QPushButton('Model',self)
        self.button_model_color.setMaximumWidth(60)
        self.button_line_color=QtGui.QPushButton('Line',self)
        self.button_line_color.setMaximumWidth(60)
        self.button_line_color.clicked.connect(self.color_choose)
        self.button_model_color.clicked.connect(self.color_choose)
        self.model_frame=QtGui.QWidget(self)
        self.line_frame=QtGui.QWidget(self)
        self.model_frame.setMaximumWidth(60)
        self.line_frame.setMaximumWidth(60)

        self.model_frame.setStyleSheet("QWidget {background-color: %s}"\
                %QtGui.QColor(LineColor).name())
        self.line_frame.setStyleSheet("QWidget {background-color: %s}"\
                %QtGui.QColor(ModelColor).name())
        self.model_frame.setGeometry(100,100,100,100)
        self.line_frame.setGeometry(100,100,100,100)
        grid_layout=QtGui.QGridLayout()
        grid_layout.addWidget(self.lbl_modelcolor,0,0)
        grid_layout.addWidget(self.lbl_linecolor,1,0)
        grid_layout.addWidget(self.button_model_color,0,1)
        grid_layout.addWidget(self.button_line_color,1,1)
        grid_layout.addWidget(self.line_frame,0,2)
        grid_layout.addWidget(self.model_frame,1,2)
        grid_layout.addWidget(self.button_ok,2,1)
        grid_layout.addWidget(self.button_default,2,2)
        self.LineColor_temp=QtGui.QColor(LineColor).name()
        self.ModelColor_temp=QtGui.QColor(ModelColor).name()

        self.setLayout(grid_layout)
        self.setWindowTitle('ColorBoard')
        self.setGeometry(300,300,220,100)
        self.show()
    def color_choose(self):
        sender=self.sender()
        button=sender.text()
        if button=='Line':
            self.LineColor_temp=QtGui.QColorDialog.getColor()
            self.model_frame.setStyleSheet("QWidget {background-color: %s}"%self.LineColor_temp.name())
        if button=='Model':
            self.ModelColor_temp=QtGui.QColorDialog.getColor()
            self.line_frame.setStyleSheet("QWidget {background-color: %s}"%self.ModelColor_temp.name())
        LineColor=QtGui.QColor(self.LineColor_temp)
        ModelColor=QtGui.QColor(self.ModelColor_temp)
    def cancel(self):
        self.close()
    def apply_color(self):
        global LineColor
        global ModelColor
        LineColor=QtGui.QColor(self.LineColor_temp)
        ModelColor=QtGui.QColor(self.ModelColor_temp)
        self.close()
    def flag_line(self):
        self.model_flag=True
    def flag_model(self):
        self.line_flag=True

class PenBox(QtGui.QWidget):
    def __init__(self):
        super(PenBox,self).__init__()
        self.initUI()
    def initUI(self):
        self.lbl_model=QtGui.QLabel('Model Pen')
        self.lbl_line=QtGui.QLabel('Line Pen ')
        self.button_ok=QtGui.QPushButton('OK',self)
        self.button_ok.clicked.connect(self.change_pen)
        self.button_cancel=QtGui.QPushButton('Cancel',self)
        self.button_cancel.clicked.connect(self.cancel)
        self.model_spinBox=QtGui.QSpinBox()
        self.model_spinBox.setMaximum(50)
        self.model_spinBox.setMinimum(1)
        self.model_spinBox.setSingleStep(1)
        self.model_spinBox.setValue(20)
        self.line_spinBox=QtGui.QSpinBox()
        self.line_spinBox.setMaximum(20)
        self.line_spinBox.setMinimum(1)
        self.line_spinBox.setSingleStep(1)
        self.line_spinBox.setValue(10)
        grid_layout=QtGui.QGridLayout()
        grid_layout.addWidget(self.lbl_model,0,0)
        grid_layout.addWidget(self.lbl_line,1,0)
        grid_layout.addWidget(self.model_spinBox,0,1)
        grid_layout.addWidget(self.line_spinBox,1,1)
        grid_layout.addWidget(self.button_ok,2,0)
        grid_layout.addWidget(self.button_cancel,2,1)
        self.setLayout(grid_layout)
        self.move(300,300)
        self.show()
    def change_pen(self):
        global LinePen
        global ModelPen
        LinePen=(self.line_spinBox.value()/10)
        ModelPen=(self.model_spinBox.value()/10)
        self.close()
    def cancel(self):
        self.close()

class Configure_Window(QtGui.QWidget):

    def __init__(self):
        super(Configure_Window,self).__init__()
        self.initUI()

    def initUI(self):
        self.lbl_prjdir=QtGui.QLabel('pro_dir')
        self.lbl_eps=QtGui.QLabel('eps')
        self.lbl_loopmax=QtGui.QLabel('loopmax')
        self.lbl_Bline_num=QtGui.QLabel('Bline num')
        self.lbl_Blevel_num=QtGui.QLabel('Blevel num')
        self.lbl_gapB_num=QtGui.QLabel('gapB num')
        self.model_choose=QtGui.QComboBox(self)
        self.model_choose.addItem('model_1')
        self.model_choose.addItem('model_2')
        self.model_choose.activated[str].connect(self.model_change)
        self.qle_eps=QtGui.QLineEdit('0.5e-6')
        self.qle_loopmax=QtGui.QLineEdit('50000')
        self.qle_Bline_num=QtGui.QLineEdit('30')
        self.qle_Blevel_num=QtGui.QLineEdit('20')
        self.qle_gapB_num=QtGui.QLineEdit('1000')
        button_ok=QtGui.QPushButton('Confirm',self)
        button_ok.clicked.connect(self.configure_load)
        button_cancel=QtGui.QPushButton('Cancel',self)
        button_cancel.clicked.connect(self.close)
        grid_layout=QtGui.QGridLayout()
        grid_layout.setContentsMargins(10,0,10,0)
        grid_layout.addWidget(self.lbl_prjdir,0,0)
        grid_layout.addWidget(self.model_choose,0,1)
        grid_layout.addWidget(self.lbl_eps,1,0)
        grid_layout.addWidget(self.qle_eps,1,1)
        grid_layout.addWidget(self.lbl_loopmax,2,0)
        grid_layout.addWidget(self.qle_loopmax,2,1)
        grid_layout.addWidget(self.lbl_Bline_num,0,3)
        grid_layout.addWidget(self.qle_Bline_num,0,4)
        grid_layout.addWidget(self.lbl_Blevel_num,1,3)
        grid_layout.addWidget(self.qle_Blevel_num,1,4)
        grid_layout.addWidget(self.lbl_gapB_num,2,3)
        grid_layout.addWidget(self.qle_gapB_num,2,4)
        grid_layout.addWidget(button_ok,3,3)
        grid_layout.addWidget(button_cancel,3,4)
        self.setLayout(grid_layout)
        self.setGeometry(300,300,400,200)
        self.show()
    def configure_load(self):
        eps_conf=self.qle_eps.text()
        eps_conf=float(eps_conf)
        fem.eps=eps_conf
        #constants.eps=eps_conf
        loopmax_conf=self.qle_loopmax.text()
        loopmax_conf=int(loopmax_conf)
        fem.loopMax=loopmax_conf
        #constants.loopMax=loopmax_conf
        Bline_num_conf=self.qle_Bline_num.text()
        Bline_num_conf=int(Bline_num_conf)
        fem.B_line_num=Bline_num_conf
        #constants.B_line_num=Bline_num_conf
        Blevel_num_conf=self.qle_Blevel_num.text()
        Blevel_num_conf=int(Blevel_num_conf)
        fem.B_level_num=Blevel_num_conf
        #constants.B_level_num=Blevel_num_conf
        gapB_num_conf=self.qle_gapB_num.text()
        gapB_num_conf=int(gapB_num_conf)
        fem.gapB_num=gapB_num_conf
        #constants.gapB_num=gapB_num_conf
        #constants.reloadConst()
        self.close()
    def model_change(self,path):
        #import constants
        global PATH
        PATH=path
        #with open('prjdir.txt','w') as f:
        #    print(PATH, file=f)
        #fem.triangle_desc = RawData('%s/B_lines_file'%PATH)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Mainwindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
