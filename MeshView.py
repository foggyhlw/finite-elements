#! py3k
# -*- coding: utf-8 -*-

''' 功能：显示区域，设置区域参数 '''

from RawData import RawData
import tkinter

class MeshView(object):
    ''' 剖分网格显示类 '''
    def __init__(self, canvas, triangle_desc, point_desc, region=0):
        super()
        self.canvas = canvas
        self.triangle_desc = triangle_desc
        self.point_desc = point_desc
        self.region = region # 只画某一区域网格，0表全部

    def drawmesh(self):
        for triangle in self.triangle_desc:
            if (self.region > 0) and (triangle[3] != self.region):
                continue # 画单区域网格
            i, j, k= map(int, triangle[0:3])
            self.canvas.create_polygon(
                    tuple(map(self.canvas_coord,
                        [self.point_desc[i-1],
                         self.point_desc[j-1],
                         self.point_desc[k-1]])),
                    outline='blue', fill='', width=1, tags=('triangle'))

    def clearmesh(self):
        self.canvas.delete('triangle')

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max([u[0] for u in self.point_desc])
        minx = min([u[0] for u in self.point_desc])
        maxy = max([u[1] for u in self.point_desc])
        miny = min([u[1] for u in self.point_desc])
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
    triangle_desc = RawData(initial_mesh_triangle_file)
    point_desc = RawData(initial_mesh_point_file)
    root =  tkinter.Tk()
    root.title('剖分网格查看程序')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    mv = MeshView(cv, triangle_desc, point_desc)
    print('command:')
    print('\tm: mesh, rm:refine mesh, 0:all region, i:region i')

    def drawmesh():
        triangle_desc.load()
        point_desc.load()
        mv.clearmesh()
        mv.calculate_coef_xy()
        mv.drawmesh()

    while True:
        cmd = input().strip()
        if 'rm' == cmd:
            triangle_desc.src = triangle_description_file
            point_desc.src = point_description_file
            drawmesh()
        elif 'm' == cmd:
            triangle_desc.src = initial_mesh_triangle_file
            point_desc.src = initial_mesh_point_file
            drawmesh()
        elif cmd.isdigit():
            mv.region = int(cmd)
            drawmesh()

    triangle_desc.reset()
    point_desc.reset()

    root.mainloop()
