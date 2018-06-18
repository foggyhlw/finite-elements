#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from EdgeView import *
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
