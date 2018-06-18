#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from SparseMatrixView import *
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
