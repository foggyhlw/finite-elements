#! py3k
# -*- coding: utf-8 -*-

from fem import *
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def main():
    print('\nsolving matrix')
    triangle_desc.load()
    point_desc.load()
    region_para.load()
    edge_desc.load()
    boundary_para.load()

    readK()
    readP()

    SOR()
    saveU()

    K.clear()
    P.clear()
    U.clear()

    triangle_desc.reset()
    point_desc.reset()
    region_para.reset()
    edge_desc.reset()
    boundary_para.reset()
    print('solving done\n')



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

if __name__ == "__main__":
    from timeit import timeit
    print('time cost:', timeit(stmt=main, number=1))
    input()

