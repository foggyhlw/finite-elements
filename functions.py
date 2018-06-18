#! py3k
# -*- coding: utf-8 -*-

# 一些简单常用的公用函数

def triangle_ijm(t): # 三角形单元顶点号
    return map(int, t[0:3])

def node_xy(i, points, unit=1): # 节点坐标，带单位转换
    return [v*unit for v in points[i-1][0:2]]

def triangle_constants(xi, yi, xj, yj, xm, ym): # 计算单元常数
    # ai, aj, am, bi, bj, bm, ci, cj, cm, delta
    return (xj * ym - xm * yj,
            xm * yi - xi * ym,
            xi * yj - xj * yi,
            yj - ym, ym - yi, yi - yj,
            xm - xj, xi - xm, xj - xi,
            ((yj-ym)*(xi-xm)-(ym-yi)*(xm-xj))/2)# 三角形单元面积

#def triangle_area(xi, yi, xj, yj, xm, ym): # 三角形面积
#    return ((yj-ym)*(xi-xm)-(ym-yi)*(xm-xj))/2

def triangle_area(xyi, xyj, xym): # 三角形面积
    return abs(((xyj[1]-xym[1])*(xyi[0]-xym[0])-(xym[1]-xyi[1])*(xym[0]-xyj[0]))/2)

def point_in_triangle(p, pi, pj, pm): # 面积法判断点是否在三角形内
    return triangle_area(pi, pj, pm) - triangle_area(
            p, pj, pm) - triangle_area(
                    pi, p, pm) - triangle_area(pi, pj, p) >= -10e-10

def triangle_du(ai, aj, am, bi, bj, bm, ci, cj, cm, delta,
        ui, uj, um): # 三角形单元中解的微分值
    dudx = (bi*ui+bj*uj+bm*um)/delta/2
    dudy = (ci*ui+cj*uj+cm*um)/delta/2
    du = (dudx**2+dudy**2)**0.5
    return dudx, dudy, du

def copydrawcoef(src, des): # 复制坐标转换系数
    des.scale_x = src.scale_x
    des.scale_y = src.scale_y
    des.offset_x = src.offset_x
    des.offset_y = src.offset_y

def average(datalist): # 求列表中数据的平均值
    return sum(datalist)/len(datalist)

def canvas_coord(x, y, cv): # 将数学坐标转化为画布坐标
    return (cv.scale_x*x+cv.offset_x, cv.scale_y*y+cv.offset_y)

def int2color(i): # 整数化为颜色表示: '#RRGGBB'
    return '#'+hex(i)[2:].rjust(6, '0')

def createCOLORS(start, end, number): # 初始颜色，终止颜色，颜色数
    # 颜色值表示为整数
    return tuple(map(int2color, range(start, end, int((end-start)/number)+1)))

if __name__ == "__main__":
    print(createCOLORS(0x0000ff, 0xff0000, 8))
    input()

