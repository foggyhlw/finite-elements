#! py3k
# -*- coding: utf-8 -*-


from RawData import RawData
import tkinter

class EdgeView(object):
    ''' 剖分网格边显示类 '''
    def __init__(self, canvas, edge_desc, point_desc, boundary=0):
        super()
        self.canvas = canvas
        self.edge_desc = edge_desc
        self.point_desc = point_desc
        self.boundary = boundary # 只画某一边界网格，0表全部

    def drawedge(self):
        for edge in self.edge_desc:
            if (self.boundary > 0) and (edge[4] != self.boundary):
                continue # 画单区域网格
            i, j= map(int, edge[0:2])
            self.canvas.create_line(
                    tuple(map(self.canvas_coord,
                        [self.point_desc[i-1],
                         self.point_desc[j-1]])),
                    fill='green', width=3, tags=('edge'))

    def clearedge(self):
        self.canvas.delete('edge')

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
    edge_desc = RawData(initial_mesh_edge_file)
    point_desc = RawData(initial_mesh_point_file)
    root =  tkinter.Tk()
    root.title('剖分边界查看程序')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    ev = EdgeView(cv, edge_desc, point_desc)
    print('command:')
    print('\te: edge, re:refine edge, 0:all boundary, i:boundary i')

    def drawedge():
        edge_desc.load()
        point_desc.load()
        ev.clearedge()
        ev.calculate_coef_xy()
        ev.drawedge()

    while True:
        cmd = input().strip()
        if 're' == cmd:
            edge_desc.src = edge_description_file
            point_desc.src = point_description_file
            drawedge()
        elif 'e' == cmd:
            edge_desc.src = initial_mesh_edge_file
            point_desc.src = initial_mesh_point_file
            drawedge()
        elif cmd.isdigit():
            ev.boundary = int(cmd)
            drawedge()

    edge_desc.reset()
    point_desc.reset()

    root.mainloop()
