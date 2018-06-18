#! py3k
# -*- coding: utf-8 -*-

from RawData import RawData
import tkinter

class BoundaryView(object):
    ''' 边界显示类 '''
    def __init__(self, canvas, boundary_desc):
        super()
        self.boundary_desc = boundary_desc
        self.canvas = canvas

    def drawboundary(self):
        ''' 画边界 '''
        for num, boundary in enumerate(self.boundary_desc, 1):
            if boundary[0] == 2:
                self.canvas.create_line(
                    tuple(map(self.canvas_coord,
                              zip(boundary[1:3], boundary[3:5]))),
                    fill='black', width=1, #arrow='last',
                    tags=('boundary', str(num)))
                #self.canvas.create_text(self.canvas_coord( 画坐标
                #    (boundary[2], boundary[4])),
                #    text='({0}, {1})'.format(boundary[2], boundary[4]),
                #    tags=('coordinate'))
        self.canvas.tag_bind('boundary', '<Button-1>',
                self.onselectboundary)

    def clearboundary(self):
        self.canvas.delete('boundary')

    def drawboundarynum(self):
        for item in self.canvas.find_withtag('boundary'):
            xy = self.canvas.coords(item)
            self.canvas.create_text(self.average(xy[0::2])+10,
                                    self.average(xy[1::2])+5,
                                    text=self.canvas.gettags(item)[1],
                                    tags=('boundarynum'))

    def clearboundarynum(self):
        self.canvas.delete('boundarynum')

    def onselectboundary(self,event):
        ''' 选择与取消选反区域 '''
        items = self.canvas.find_closest(event.x, event.y)
        for item in items:
            if float(self.canvas.itemcget(item, 'width')) < 3:
                self.canvas.itemconfigure(item, width=3)
            else:
                self.canvas.itemconfigure(item, width=1)
        
    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max([max(u[1:3]) for u in self.boundary_desc])
        minx = min([min(u[1:3]) for u in self.boundary_desc])
        maxy = max([max(u[3:5]) for u in self.boundary_desc])
        miny = min([min(u[3:5]) for u in self.boundary_desc])
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

if __name__ == "__main__":
    from constants import *
    boundary_desc = RawData(boundary_description_file)
    root =  tkinter.Tk()
    root.title('模型边界')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    bv = BoundaryView(cv, boundary_desc)
    from timeit import timeit
    print('preparing time:', timeit(boundary_desc.load, number=1))
    bv.calculate_coef_xy()
    print('drawing boundary time:', timeit(bv.drawboundary, number=1))
    print('drawing num time:', timeit(bv.drawboundarynum, number=1))
    print('reset time:', timeit(boundary_desc.reset, number=1))
    root.mainloop()
