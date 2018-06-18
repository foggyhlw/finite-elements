#! py3k
# -*- coding: utf-8 -*-

from fem import *

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def main():
    print('\ncalculating B lines')
    triangle_desc.load()
    point_desc.load()
    readU()

    calculate_B_lines()
    print('1.a', B_lines_file)
    print('1.b', B_lines.src)
    B_lines.save()
    B_lines.reset()
    U.clear()

    triangle_desc.reset()
    point_desc.reset()
    print('B lines done\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

if __name__ == "__main__":
    from timeit import timeit
    print('time cost:', timeit(stmt=main, number=1))
    input()

