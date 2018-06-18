#! py3k
# -*- coding: utf-8 -*-

from RegionView import RegionView
from BoundaryView import BoundaryView
from RawData import RawData
import tkinter

class DrawLinesView(object):
    ''' 画线显示类 '''
    def __init__(self, canvas, lines):
        super()
        self.lines = lines
        self.canvas = canvas

    def drawlines(self):
        ''' 画线 '''
        for num, line in enumerate(self.lines, 1):
            for i in range(0, len(line), 4):
                self.canvas.create_line(
                    self.canvas_coord(line[i:i+2]),
                    self.canvas_coord(line[i+2:i+4]),
                    fill='black', width=1,
                    tags=('lines'))
    def clearlines(self):
        self.canvas.delete('lines')

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max([max(u[0::2]) for u in self.lines])
        minx = min([min(u[0::2]) for u in self.lines])
        maxy = max([max(u[1::2]) for u in self.lines])
        miny = min([min(u[1::2]) for u in self.lines])
        self.scale_x = 0.8*float(self.canvas['width']) / (maxx-minx)
        self.scale_y = -0.8*float(self.canvas['height']) / (maxy-miny)
        self.offset_x = -0.8*float(self.canvas['width'])*minx/(maxx-minx
                )+0.1*float(self.canvas['width'])
        self.offset_y = 0.8*float(self.canvas['height'])*miny/(maxy-miny
                )+0.9*float(self.canvas['height'])

    def canvas_coord(self, xy):
        ''' 将数学坐标转化为画布坐标 '''
        return (self.scale_x*xy[0]+self.offset_x,
                self.scale_y*xy[1]+self.offset_y)

    def average(self, datalist):
        ''' 求列表中数据的平均值 '''
        return sum(datalist)/len(datalist)

def copydrawcoef(src, des):
    des.scale_x = src.scale_x
    des.scale_y = src.scale_y
    des.offset_x = src.offset_x
    des.offset_y = src.offset_y

if __name__ == "__main__":
    from constants import *
    lines = RawData(B_lines_file)
    region_desc = RawData(region_description_file)

    root =  tkinter.Tk()
    root.title('磁力线')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()

    rv = RegionView(cv, region_desc)
    dlv = DrawLinesView(cv, lines)

    region_desc.load()
    lines.load()
    
    rv.calculate_coef_xy()
    copydrawcoef(rv, dlv)

    rv.drawregion()
    dlv.drawlines()
    
    region_desc.reset()
    lines.reset()
    root.mainloop()
