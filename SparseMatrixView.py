#! py3k
# -*- coding: utf-8 -*-

from RawData import RawData
from itertools import product
import tkinter

class SparseMatrixView(object):
    def __init__(self, canvas, triangle_desc, point_desc):
        super()
        self.canvas = canvas
        self.triangle_desc = triangle_desc
        self.point_desc = point_desc

    def drawpoints(self):
        x, y = [0.0]*2 #XXX
        for t in self.triangle_desc:
            for i, j in product(t[0:3], repeat=2):
                x, y = self.canvas_coord((i, j))
                self.canvas.create_oval(x-0.5, y-0.5, x+0.5, y+0.5,
                        tags='point')
        self.canvas.create_rectangle(self.canvas_coord((0, 0)),
                self.canvas_coord((len(self.point_desc),
                    len(self.point_desc))), outline='red')
    def drawpoints2(self):
        from collections import defaultdict
        index = defaultdict(defaultdict)
        for t in self.triangle_desc:
            for i, j in product(map(int, t[0:3]), repeat=2):
                index[i][j] = 1
        for i in index.keys():
            for j in index.keys():
                x, y = self.canvas_coord((i, j))
                self.canvas.create_oval(x-0.5, y-0.5, x+0.5, y+0.5,
                        tags='point')

    def clearpoints(self):
        self.canvas.delete('point')

    def profile(self):
        ''' 统计生成矩阵的稀疏程度 '''
        n = len(self.point_desc)
        print("total node number: {0}".format(n))
        from collections import defaultdict
        index = defaultdict(defaultdict)
        for t in self.triangle_desc:
            for i, j in product(map(int, t[0:3]), repeat=2):
                index[i][j] = 1
        count = 0
        for i in index.keys():
            for j in index[i].keys():
                count = count + 1
        print("full matrix size:", n**2)
        print("not-zero-element number:", count)
        print("sparse ratio:", count/n**2)

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        n = len(self.point_desc)
        maxx = n+1
        minx = -1
        maxy = n+1
        miny = -1
        self.scale_x = 0.8*float(self.canvas['width']) / (maxx-minx)
        self.scale_y = 0.8*float(self.canvas['height']) / (maxy-miny)
        self.offset_x = 0.1*float(self.canvas['width'])
        self.offset_y = 0.1*float(self.canvas['height'])

    def canvas_coord(self, xy):
        ''' 将数学坐标转化为画布坐标 '''
        return (self.scale_x*xy[0]+self.offset_x,
                self.scale_y*xy[1]+self.offset_y)

if __name__ == "__main__":
    from constants import *
    from timeit import timeit
    triangle_desc = RawData(triangle_description_file)
    point_desc = RawData(point_description_file)
    root = tkinter.Tk()
    root.title('系数矩阵稀疏度分析')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    smv = SparseMatrixView(cv, triangle_desc, point_desc)
    triangle_desc.load()
    point_desc.load()
    smv.calculate_coef_xy()
    t = timeit(stmt=smv.drawpoints, number=1)
    print('spend time in drawpoints:', t)
    t = timeit(stmt=smv.profile, number=1)
    print('spend time in profile:', t)

    triangle_desc.reset()
    point_desc.reset()
    root.mainloop()
