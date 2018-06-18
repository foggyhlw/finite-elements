#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from RegionView import *
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
