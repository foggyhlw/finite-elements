#! py3k
# -*- coding: utf-8 -*-
prjdir = 'model_1' # 工程目录
tpl = '{0}/{1}' # 文件路径模版
point_description_file = tpl.format(prjdir, 'pde_refine_p.txt') # 剖分点文件
edge_description_file = tpl.format(prjdir, 'pde_refine_e.txt') # 边界剖分文件
triangle_description_file = tpl.format(prjdir, 'pde_refine_t.txt') # 剖分三角形文件

initial_mesh_point_file = tpl.format(prjdir, 'pde_p.txt') # 初始剖分点文件
initial_mesh_edge_file = tpl.format(prjdir, 'pde_e.txt') # 初始剖分边文件
initial_mesh_triangle_file = tpl.format(prjdir, 'pde_t.txt') # 初始剖分三角形文件

region_description_file = tpl.format(prjdir, 'pde_gd.txt') # 模型实体数据文件
region_parameter_file = tpl.format(prjdir, 'region_parameter.txt') # 模型参数文件
boundary_description_file = tpl.format(prjdir, 'pde_g.txt') # 模型边界数据文件
boundary_parameter_file = tpl.format(prjdir, 'boundary_parameter.txt') # 模型边界条件

K_file = tpl.format(prjdir, 'K_file.txt') # 保存系数矩阵的的文件
P_file = tpl.format(prjdir, 'P_file.txt') # 保存向端向量的文件
U_file = tpl.format(prjdir, 'U_file.txt') # 保存解向量的文件
B_file = tpl.format(prjdir, 'B_file.txt') # 保存三角形单元磁密数值的文件
B_lines_file = tpl.format(prjdir, 'B_lines_file.txt') # 磁密线（即等A线）坐标数据

gapB_file = tpl.format(prjdir, 'gapB_file.txt') # 气隙磁密数据

def reloadConst():
	pass

from math import pi # 圆周率
Mu0 = 4*pi*10**-7 # 真空磁导率
LengthUnit = 0.01 # 长度单位比例，厘米

# SOR迭代法解方程的参数
omg = 1 # 松驰因子
eps = 0.5e-5 # 精度
loopMax = 50000 # 迭代次数上限

B_line_num = 50 # 磁力线条数
B_level_num = 20 # 磁密分级数目，云图颜色数目
gap_start_xy = 0, 4.05 # 气隙起始坐标
gap_end_xy = 12, 4.05 # 气隙终止坐标
if prjdir == 'model_1':
    gap_start_xy = -3.6, 0.9
    gap_end_xy = 3.6, 0.9
gapB_num = 1000 # 气隙磁密数据数目

if __name__ == "__main__":
    tpl = '{0}/{1}'
    x = tpl.format(prjdir, 'x')
    print(prjdir)
    print(x)
    input()

