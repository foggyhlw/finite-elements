#! py3k
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from constants import *
    from MeshView import *
    triangle_desc = RawData(initial_mesh_triangle_file)
    point_desc = RawData(initial_mesh_point_file)
    root =  tkinter.Tk()
    root.title('剖分网格查看程序')
    cv = tkinter.Canvas(root, bg='white', width=600, height=600)
    cv.pack()
    mv = MeshView(cv, triangle_desc, point_desc)
    print('command:')
    print('\tm: mesh, rm:refine mesh, 0:all region, i:region i')

    def drawmesh():
        triangle_desc.load()
        point_desc.load()
        mv.clearmesh()
        mv.calculate_coef_xy()
        mv.drawmesh()

    while True:
        cmd = input().strip()
        if 'rm' == cmd:
            triangle_desc.src = triangle_description_file
            point_desc.src = point_description_file
            drawmesh()
        elif 'm' == cmd:
            triangle_desc.src = initial_mesh_triangle_file
            point_desc.src = initial_mesh_point_file
            drawmesh()
        elif cmd.isdigit():
            mv.region = int(cmd)
            drawmesh()

    triangle_desc.reset()
    point_desc.reset()

    root.mainloop()
