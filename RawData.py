#! py3k
# -*- coding: utf-8 -*-

import os

class RawData(list):
    ''' 原始数据访问接口，有用数据地址从1开始 '''
    def __init__(self, src):
        super() #list.__init__(self)
        self.src = src
        # 使有用数据地址从0开始

    def exists(self, filename=None):
        ''' 验证文件存在否 '''
        if filename==None:
            return os.path.exists(self.src)
        return os.path.exists(filename)

    def empty(self):
        ''' 验证是否保存有数据 '''
        return len(self) > 0 # 从0开始

    def load(self):
        ''' 从源载入数据 '''
        with open(self.src) as infile:
            self.reset()
            for line in infile:
                #self.append(line.split())
                self.append(list(map(float, line.split())))

    def reset(self):
        ''' 重置清空数据 '''
        del self[:] # 保留第x位

    def save(self):
        ''' 保存数据到源文件 '''
        with open(self.src, mode='w') as outfile:
            for i in self: # 保存地址从0开始以后的数据
                print('\t'.join(map(str, i)), end='\n', file=outfile)

