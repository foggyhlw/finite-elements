#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from CloudView import *
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
