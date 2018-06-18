#!/usr/bin/python3
import matplotlib.pyplot as plt
from PyQt4 import QtGui,QtCore
f=open('pde_gd.txt')
axis_x=[]
axis_y=[]
while True:
    line=f.readline()
    if line:
        global axis_x
        global axis_y
        a=line.split('\t')
        inta=[float(i) for i in a]
        num=int(inta[1])
        i=0;
        while i<num:
            axis_x.append(inta[i+2])
            axis_y.append(inta[i+2+num])
            i=i+1
    else:
        break
plt.plot(axis_x,axis_y)
plt.show()
f.close()
