#! py3k
# -*- coding: utf-8 -*-

''' 功能：画函数图 '''

from functions import *
from RawData import RawData
import tkinter

class PlotView(object):
    ''' 画函数图 '''
    def __init__(self, canvas, funxy):
        super()
        self.canvas = canvas
        self.funxy = funxy # 函数的横坐标和纵坐标

    def plot(self):
        self.canvas.create_line(*map(self.canvas_coord, self.funxy),
                fill='blue')
        self.canvas.create_line(*map(self.canvas_coord,
            ((-20, 0), (20, 0))), fill='red')
        self.canvas.create_line(*map(self.canvas_coord,
            ((0, -10), (0, 10))), fill='red')

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max(u[0] for u in self.funxy)
        minx = min(u[0] for u in self.funxy)
        maxy = max(u[1] for u in self.funxy)
        miny = min(u[1] for u in self.funxy)
        self.scale_x = 0.8*float(self.canvas['width']) / (maxx-minx)
        self.scale_y = -0.8*float(self.canvas['height']) / (maxy-miny)
        self.offset_x = -float(self.canvas['width'])*minx/(maxx-minx)
        self.offset_y = 0.9*float(self.canvas['height'])*maxy/(maxy-miny)

    def canvas_coord(self, xy):
        ''' 将数学坐标转化为画布坐标 '''
        return (self.scale_x*xy[0]+self.offset_x,
                self.scale_y*xy[1]+self.offset_y)

if __name__ == "__main__":
    from constants import *
    from BoundaryView import BoundaryView
    gapB = RawData(gapB_file)
    boundary_desc = RawData(boundary_description_file)

    root =  tkinter.Tk()
    root.title('气隙磁密')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    pv = PlotView(cv, gapB)
    bv = BoundaryView(cv, boundary_desc)

    gapB.load()
    boundary_desc.load()

    pv.calculate_coef_xy()
    bv.calculate_coef_xy()
    pv.scale_x, pv.offset_x = bv.scale_x, bv.offset_x
    pv.offset_y = bv.canvas_coord(gap_start_xy)[1] # 偏移到气隙线上
    pv.scale_y = pv.scale_y/4

    pv.plot()
    bv.drawboundary()

    gapB.reset()
    boundary_desc.reset()
    root.mainloop()



