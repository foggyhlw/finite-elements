#! py3k
# -*- coding: utf-8 -*-

# 构造初始值为零的稀疏矩阵和向量
from collections import defaultdict
def zero(): # 零函数
    return 0

def defaultzerodict(): # 零字典
    return defaultdict(zero)

def SparseMatrix(): # 稀疏矩阵
    return defaultdict(defaultzerodict)

def SparseVector(): # 稀疏向量
    return defaultzerodict()

########################################################
########################################################

class SymmtryVariableBandSparseMatrix(object):
    ''' 稀疏矩阵，不对称矩阵，变带宽 '''
    def __init__(self, data, diagindex, leftsize, rightsize):
        super()
        self.data = data # 按行存储数据
        self.diagindex = diagindex # 主对角元的索引号
        self.leftsize = leftsize # 对角元左边连续非零元数
        self.rightsize = rightsize # 右边

    def set(self, i, j, val):
        di, li, ri = self.diagindex[i], -self.leftsize[i], self.rightsize[i]
        if li <= j-i <= ri:
            self.data[j-i+di] = val
            return self.data[j-i+di]
        else:
            return 0

    def get(self, i, j):
        di, li, ri = self.diagindex[i], self.leftsize[i], self.rightsize[i]
        if -li <= j-i <= ri:
            return self.data[j-i+di]
        else:
            return 0

class SymmtryFixBandSparseMatrix(object):
    ''' 稀疏矩阵，对称矩阵，变带宽 '''
    def __init__(self, data, diagindex, leftsize):
        super()
        self.data = data # 按行存储数据，下三角
        self.diagindex = diagindex # 主对角元的索引号
        self.leftsize = leftsize # 对角元左边连续非零元数

    def set(self, i, j, val):
        if i < j:
            i, j = j, i
        di, li = self.diagindex[i], -self.leftsize[i]
        if li <= j-i <= 0:
            self.data[j-i+di] = val
            return self.data[j-i+di]
        else:
            return 0

    def get(self, i, j):
        if i < j:
            i, j = j, i
        di, li = self.diagindex[i], -self.leftsize[i]
        if li <= j-i <= 0:
            return self.data[j-i+di]
        else:
            return 0

class CompressRowSparseMatrix(object):
    ''' 稀疏矩阵，依行压缩，坐标存储 '''
    def __init__(self, data, index):
        super()
        self.data = data # 数据，按行压缩存储
        self.index = index # 行列索引

    def set(self, i, j, val):
        k = self.index[i].index(j)
        self.data[i][k] = val
        return self.data[i][k]

    def get(self, i, j):
        try:
            k = self.index[i].index(j)
            return self.data[i][k]
        except ValueError:
            return 0

class Vector_P(list):
    ''' 向量 '''
    def __init__(self, data):
        super()
        self.data = data

    def set(self, i, val):
        data[i] = val
        return self.data[i]

    def get(self, i):
        return data[i]

def printmatrix(m, n):
    for i in range(n):
        for j in range(n):
            print(m.get(i, j), end=',')
        print()

