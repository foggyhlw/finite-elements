#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from PlotView import *
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
