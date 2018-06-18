#! py3k
# -*- coding: utf-8 -*-


from fem import *
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def main():
    print('\ncalculating B')
    triangle_desc.load()
    point_desc.load()

    readU()
    calculate_triangle_B()
    B.save()
    B.reset()
    U.clear()

    triangle_desc.reset()
    point_desc.reset()
    print('B calculating done\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

if __name__ == "__main__":
    from timeit import timeit
    print('time cost:', timeit(stmt=main, number=1))
    input()

