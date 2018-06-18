#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from DrawLinesView import *
    lines = RawData(B_lines_file)
    region_desc = RawData(region_description_file)

    root =  tkinter.Tk()
    root.title('磁力线')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()

    rv = RegionView(cv, region_desc)
    dlv = DrawLinesView(cv, lines)

    region_desc.load()
    lines.load()
    
    rv.calculate_coef_xy()
    copydrawcoef(rv, dlv)

    rv.drawregion()
    dlv.drawlines()
    
    region_desc.reset()
    lines.reset()
    root.mainloop()
