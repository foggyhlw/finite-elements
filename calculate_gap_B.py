#! py3k
# -*- coding: utf-8 -*-

from fem import *
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def main():
    print('\ncalculating gap B')
    triangle_desc.load()
    point_desc.load()
    B.load()

    gapBdata(gap_start_xy, gap_end_xy, gapB_num)
    gapB.save()
    gapB.reset()

    B.reset()
    triangle_desc.reset()
    point_desc.reset()

    print('gap B done\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

if __name__ == "__main__":
    from timeit import timeit
    print('time cost:', timeit(stmt=main, number=1))
    input()

