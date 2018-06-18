#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from BoundaryView import *
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
