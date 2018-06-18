#! py3k
# -*- coding: utf-8 -*-

''' 功能：显示区域，设置区域参数 '''

from RawData import RawData
import tkinter

class RegionView(object):
    ''' 区域显示类 '''
    def __init__(self, canvas, region_desc):
        super()
        self.canvas = canvas
        self.region_desc = region_desc

    def drawregion(self):
        ''' 画区域 '''
        for num, region in enumerate(self.region_desc, 1):
            if region[0] in (2, 3):
                n = int(region[1])
                self.canvas.create_polygon(
                    tuple(map(self.canvas_coord,
                              zip(region[2:2+n], region[2+n:2+n+n]))),
                    fill='', outline='blue',
                    tags=('region', str(num)))
        self.canvas.tag_bind('region', '<Button-1>', self.onselectregion)

    def clearregion(self):
        ''' 删除区域 '''
        self.canvas.delete('region')

    def drawregionnum(self):
        ''' 标注区域号 '''
        for item in self.canvas.find_withtag('region'):
            xy = self.canvas.coords(item)
            self.canvas.create_text(self.average(xy[0::2]),
                                    self.average(xy[1::2]),
                                    text=self.canvas.gettags(item)[1],
                                    tags=('regionnum'))

    def clearregionnum(self):
        ''' 删除区域号 '''
        self.canvas.delete('regionnum')

    def drawcoordinate(self):
        ''' 画出顶点坐标 '''
        coordinate = set()
        for region in self.region_desc:
            if region[0] in (2, 3):
                n = int(region[1])
                for p in zip(region[2:2+n], region[2+n:2+n+n]):
                    coordinate.add(p)
        #print(coordinate)
        for xy in coordinate:
            x, y = self.canvas_coord(xy)
            self.canvas.create_text(x-5, y+5,
                    text='({0[0]:#4.2},{0[1]:#4.2})'.format(xy),
                    tags=('coordinate'))

    def clearcoordinate(self):
        self.canvas.delete('coordinate')

    def onselectregion(self, event):
        ''' 选择与取消选反高亮区域 '''
        items = self.canvas.find_closest(event.x, event.y)
        for item in items:
            if not self.canvas.itemcget(item, 'fill'):
                self.canvas.itemconfigure(item, fill='grey')
            else:
                self.canvas.itemconfigure(item, fill='')

    def calculate_coef_xy(self):
        ''' 计算坐标变化的比例系数和偏移系数 '''
        maxx = max(max(u[2:2+int(u[1])]) for u in self.region_desc)
        minx = min(min(u[2:2+int(u[1])]) for u in self.region_desc)
        maxy = max(max(u[2+int(u[1]):2+int(u[1])+int(u[1])])
                   for u in self.region_desc)
        miny = min(min(u[2+int(u[1]):2+int(u[1])+int(u[1])])
                   for u in self.region_desc)
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
    region_desc = RawData(region_description_file)
    root =  tkinter.Tk()
    root.title('模型区域')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    rv = RegionView(cv, region_desc)
    region_desc.load()
    rv.calculate_coef_xy()
    rv.drawregion()
    rv.drawregionnum()
    rv.drawcoordinate()
    region_desc.reset()
    root.mainloop()
