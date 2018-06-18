#! py3k
# -*- coding: utf-8 -*-

from RawData import RawData
from SparseMatrix import SparseMatrix
from SparseMatrix import SparseVector
from math import cos
from math import sin
import os

from constants import *
from functions import *

# RawData类地址从0开始
#region_desc = RawData(region_description_file)
region_para = RawData(region_parameter_file)
#boundary_desc = RawData(boundary_description_file)
boundary_para = RawData(boundary_parameter_file)
point_desc = RawData(point_description_file)
edge_desc = RawData(edge_description_file)
triangle_desc = RawData(triangle_description_file)

# 构造初始值为零的稀疏矩阵和向量，地址从1开始
K = SparseMatrix()
P = SparseVector()
U = SparseVector()

B = RawData(B_file)
B_lines = RawData(B_lines_file)
gapB = RawData(gapB_file)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

def MakeHomoConditionMatrix():
    ''' 根据剖分生成齐次边界条件矩阵 '''
    i, j, m = [0]*3 #XXX
    ai, aj, am, bi, bj, bm, ci, cj, cm, delta = [0.0]*10 #XXX
    beta, f, Hc, theta, cst, snt = [0.0]*6 #XXX
    for t in triangle_desc:
        i, j, m = triangle_ijm(t)
        (ai, aj, am, bi, bj, bm, ci, cj, cm, delta
                ) = triangle_constants(
                        *node_xy(i, point_desc, LengthUnit)
                        + node_xy(j, point_desc, LengthUnit)
                        + node_xy(m, point_desc, LengthUnit))
        assert delta > 0

        beta, f = 1/Mu0, 0 # 磁阻率，电流密度
        #Mu, f = Mu0, 0
        para = region_para[int(t[3])-1]
        if 1 == para[0]: # 一般区域
            beta = beta/para[1]
            #Mu = Mu*para[1]
            f = para[2]
            P[i] = P[i] + f * delta / 3
            P[j] = P[j] + f * delta / 3
            P[m] = P[m] + f * delta / 3
        elif 2 == para[0]: # 永磁区域
            beta = beta/para[1]
            #Mu = Mu*para[1]
            Hc = para[2]
            theta = para[3]*pi/180 # 角度转弧度
            cst = cos(theta)
            snt = sin(theta)
            P[i] = P[i] + (ci*cst-bi*snt)*Hc/2 # 直接处理法
            P[j] = P[j] + (cj*cst-bj*snt)*Hc/2
            P[m] = P[m] + (cm*cst-bm*snt)*Hc/2
        else: # 其它类型区域默认处理
            P[i] = P[i] + f * delta / 3
            P[j] = P[j] + f * delta / 3
            P[m] = P[m] + f * delta / 3

        K[i][i] = K[i][i] + (bi**2 + ci**2) * beta / delta / 4 # 单元分析
        K[j][j] = K[j][j] + (bj**2 + cj**2) * beta / delta / 4 # 并合成
        K[m][m] = K[m][m] + (bm**2 + cm**2) * beta / delta / 4
        K[i][j] = K[i][j] + (bi * bj + ci * cj) * beta / delta / 4
        K[j][i] = K[j][i] + (bi * bj + ci * cj) * beta / delta / 4
        K[j][m] = K[j][m] + (bj * bm + cj * cm) * beta / delta / 4
        K[m][j] = K[m][j] + (bj * bm + cj * cm) * beta / delta / 4
        K[m][i] = K[m][i] + (bm * bi + cm * ci) * beta / delta / 4
        K[i][m] = K[i][m] + (bm * bi + cm * ci) * beta / delta / 4

def treat_1type(j, uj):
    j = int(j) # 处理第一类边界条件上的点
    assert j > 0
    for i in K.keys():
        if j in K[i].keys():
            P[i] = P[i] - K[i][j] * uj
            del K[i][j]
    if j in K.keys():
        del K[j]
        K[j][j] = 1
        P[j] = uj

def treat_2type(j, qj, sj):
    j = int(j) # 处理第二类边界条件上的点，第二个布尔条件保证
    assert j > 0
    if (j in K.keys()) and (len(K) == 1): # 不处理已知值的节点
        P[j] = P[j] + qj*sj/2

def TreatBoundaryPara():
    ''' 处理边界条件 '''
    para, x1, y1, x2, y2, s = [0.0]*6 #XXX
    for e in edge_desc:
        assert e[4] > 0
        para = boundary_para[int(e[4])-1]
        if para[0] == 1:
            treat_1type(e[0], para[1])
            treat_1type(e[1], para[1])
        elif para[0] == 2:
            x1, y1 = node_xy(int(e[0]-1), point_desc, LengthUnit)
            x2, y2 = node_xy(int(e[1]-1), point_desc, LengthUnit)
            s = ((x1-x2)**2 + (y1-y2)**2)**0.5
            treat_2type(e[0], para[1], s)
            treat_2type(e[1], para[1], s)

def saveK():
    with open(K_file, mode='w') as fout:
        for i in K.keys():
            print(', '.join(map(str, K[i].keys())), end=':\t', file=fout)
            print(', '.join(map(str, K[i].values())),
                    end='\n', file=fout)

def readK():
    with open(K_file) as fin:
        K.clear()
        for i, line in enumerate(fin, 1):
            strj, strd = line.split(':\t')
            #print(i, repr(strj), repr(strd))
            for j, d in zip(map(int, strj.split(', ')),
                    map(float, strd.split(', '))):
                K[i][j] = d

def saveP():
    with open(P_file, mode='w') as fout:
        for i in P.keys():
            print(P[i], end='\n', file=fout)

def readP():
    with open(P_file) as fin:
        P.clear()
        for i, line in enumerate(fin, 1):
            P[i] = float(line)

def SOR():
    ''' 超松驰迭代法解稀疏矩阵方程 '''
    assert 0 < omg < 2
    ui0 = 0
    norm, s = 0.0, 0.0 #XXX
    for count in range(loopMax):
        norm = 0
        for i in K.keys():
            s = 0
            for j in K[i].keys():
                if j == i:
                    continue
                s = s + K[i][j] * U[j]
            ui0 = (1-omg)*U[i] + omg*(P[i]-s)/K[i][i]
            norm = max(abs(ui0 - U[i]), norm)
            U[i] = ui0
        if count % 500 == 0:
            print('norm: ', norm)
        if norm < eps:
            print('norm: ', norm)
            break
    print('computing times:', count)

def saveU():
    with open(U_file, mode='w') as fout:
        for i in U.keys():
            print(U[i], end='\n', file=fout)

def readU():
    with open(U_file) as fin:
        U.clear()
        for i, line in enumerate(fin, 1):
            U[i] = float(line)

def calculate_triangle_B():
    ''' 计算所有三角形单元中磁密B的值 '''
    B.reset()
    i, j, m = [0]*3 #XXX
    for t in triangle_desc:
        i, j, m = triangle_ijm(t)
        B.append(triangle_du(*triangle_constants(
                *node_xy(i, point_desc, LengthUnit) + node_xy(
                    j, point_desc, LengthUnit) + node_xy(
                        m, point_desc, LengthUnit)) + (U[i], U[j], U[m])))

def calculate_B_lines():
    ''' 计算磁力线，即B线，即等A线 '''
    maxu = max(U.values())
    minu = min(U.values())
    stepu = (maxu-minu) / B_line_num
    B_lines.reset()
    points = list()
    i, j, m = [0]*3 #XXX
    uk, ui, uj, um = [0]*4 #XXX
    xi, yi, xj, yj, xm, ym = [0.0]*6 #XXX
    ai, aj, am, bi, bj, bm, ci, cj, cm, delta = [0.0]*10 #XXX
    a11, a12, b1, a21, a22, b2 = [0.0]*6 #XXX
    x, y = [0.0]*2 #XXX
    for k in range(0, B_line_num):
        uk = minu+stepu*k
        B_lines.append([])
        for t in triangle_desc:
            i, j, m = triangle_ijm(t)
            ui, uj, um = U[i], U[j], U[m]
            if not(min(ui, uj, um) <= uk <= max(ui, uj, um)):
                continue
            xi, yi = node_xy(i, point_desc, LengthUnit)
            xj, yj = node_xy(j, point_desc, LengthUnit)
            xm, ym = node_xy(m, point_desc, LengthUnit)
            ai, aj, am, bi, bj, bm, ci, cj, cm, delta = triangle_constants(
                    xi, yi, xj, yj, xm, ym)
            a11 = bi*ui+bj*uj+bm*um # 解方程得到在三角形边及顶点上与指定值
            a12 = ci*ui+cj*uj+cm*um # 相等的点坐标, 单位转为原始数据单位
            b1 = 2*delta*uk-ai*ui-aj*uj-am*um
            del points[:]
            if min(ui, uj) <= uk < max(ui, uj):
                a21 = yj-yi
                a22 = xi-xj
                b2 = xi*yj-xj*yi
                x = (b1*a22-b2*a12)/(a11*a22-a12*a21)
                y = (a11*b2-a21*b1)/(a11*a22-a12*a21)
                points.append(x)
                points.append(y)
            if min(uj, um) <= uk < max(uj, um):
                a21 = ym-yj
                a22 = xj-xm
                b2 = xj*ym-xm*yj
                x = (b1*a22-b2*a12)/(a11*a22-a12*a21)
                y = (a11*b2-a21*b1)/(a11*a22-a12*a21)
                points.append(x)
                points.append(y)
            if min(um, ui) <= uk < max(um, ui):
                a21 = yi-ym
                a22 = xm-xi
                b2 = xm*yi-xi*ym
                x = (b1*a22-b2*a12)/(a11*a22-a12*a21)
                y = (a11*b2-a21*b1)/(a11*a22-a12*a21)
                points.append(x)
                points.append(y)
            if len(points) >=4:
                for v in range(4):
                    B_lines[k].append(points[v]/LengthUnit)

def gapBdata(xy1, xyn, n):
    ''' 计算气隙磁密 '''
    x1, y1 = xy1 # 起点
    xn, yn = xyn # 终点
    s = ((xn-x1)**2+(yn-y1)**2)**0.5 # 直线长
    kx, ky = (xn-x1)/s, (yn-y1)/s # cos, sin, 直线方向
    ds = s/(n-1) # 直线长度步长
    gapB.reset()
    x, y = [0.0]*2 #XXX
    i, j, m = [0]*3 #XXX 假设能提高性能
    for iii in range(0, n):
        x, y = x1+iii*ds*kx, y1+iii*ds*ky
        gapB.append([]) # 以弧长为参数的直线参数公式
        for k, t in enumerate(triangle_desc, 0):
            i, j, m = triangle_ijm(t) # 寻找点所在的三角形单元号
            if point_in_triangle((x, y), node_xy(i, point_desc),
                    node_xy(j, point_desc),
                    node_xy(m, point_desc)):
                gapB[-1].append(x) # 存入横坐标
                gapB[-1].append(B[k][-1])
                break

if __name__ == "__main__":
    #from timeit import timeit
    #print('time cost:', timeit(stmt=main, number=1))
    print('fem functions')
    input()

