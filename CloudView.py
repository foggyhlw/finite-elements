#! py3k
# -*- coding: utf-8 -*-

''' 功能：画磁密云图 '''

from functions import *
from RawData import RawData
import tkinter

class CloudView(object):
    ''' 画磁密云图 '''
    def __init__(self, canvas, triangle_desc, point_desc, B, COLORS):
        super()
        self.canvas = canvas
        self.triangle_desc = triangle_desc
        self.point_desc = point_desc
        self.B = B
        self.COLORS = COLORS

    def drawcloud(self):
        maxB = max(u[-1] for u in self.B)
        minB = min(u[-1] for u in self.B)
        n = len(self.COLORS)
        stepB = 1.01*(maxB-minB)/n # 步长稍大以解决最大值溢出区间问题
        for k, t in enumerate(self.triangle_desc, 0):
            i, j, m= triangle_ijm(t)
            self.canvas.create_polygon(
                    tuple(map(self.canvas_coord,
                        [self.point_desc[i-1],
                         self.point_desc[j-1],
                         self.point_desc[m-1]])),
                    outline='', width=1, 
                    fill=self.COLORS[int((self.B[k][-1]-minB)/stepB)],
                    tags=('cloud'))
        # 图例
        legendbasex = float(self.canvas['width'])*0.9
        legendbasey = 0.15*float(self.canvas['height'])
        for k, color in enumerate(self.COLORS, 0):
            self.canvas.create_text(legendbasex,
                    legendbasey+k*15,
                    text='{0:#4.4}~{1:#4.4}T'.format(
                        minB+k*stepB, minB+(k+1)*stepB),
                    fill=color)

    def clearcloud(self):
        self.canvas.delete('cloud')

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max([u[0] for u in self.point_desc])
        minx = min([u[0] for u in self.point_desc])
        maxy = max([u[1] for u in self.point_desc])
        miny = min([u[1] for u in self.point_desc])
        self.scale_x = 0.8*float(self.canvas['width']) / (maxx-minx)
        self.scale_y = -0.8*float(self.canvas['height']) / (maxy-miny)
        self.offset_x = -0.8*float(self.canvas['width'])*minx/(maxx-minx
                )+0.01*float(self.canvas['width'])
        self.offset_y = 0.8*float(self.canvas['height'])*miny/(maxy-miny
                )+0.9*float(self.canvas['height'])

    def canvas_coord(self, xy):
        ''' 将数学坐标转化为画布坐标 '''
        return (self.scale_x*xy[0]+self.offset_x,
                self.scale_y*xy[1]+self.offset_y)

if __name__ == "__main__":
    from constants import *
    triangle_desc = RawData(triangle_description_file)
    point_desc = RawData(point_description_file)
    B = RawData(B_file)

    root =  tkinter.Tk()
    root.title('磁密云图')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    mv = CloudView(cv, triangle_desc, point_desc,
            B, createCOLORS(0x0000ff, 0xff0000, B_level_num))

    triangle_desc.load()
    point_desc.load()
    B.load()

    mv.calculate_coef_xy()
    mv.drawcloud()

    triangle_desc.reset()
    point_desc.reset()
    B.reset()

    root.mainloop()
