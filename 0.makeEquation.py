#! py3k
# -*- coding: utf-8 -*-

from fem import *
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def main():
    print('\nmaking matrix')
    triangle_desc.load()
    point_desc.load()
    region_para.load()
    edge_desc.load()
    boundary_para.load()

    MakeHomoConditionMatrix()
    TreatBoundaryPara()
    saveK()
    saveP()
    K.clear()
    P.clear()

    triangle_desc.reset()
    point_desc.reset()
    region_para.reset()
    edge_desc.reset()
    boundary_para.reset()
    print('matrix done\n')
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

if __name__ == "__main__":
    from timeit import timeit
    print('time cost:', timeit(stmt=main, number=1))
    input()

