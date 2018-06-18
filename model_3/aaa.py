#!/usr/bin/python3
f=open('pde_p.txt')
ch=[]
while True:
    a=f.readline()
    if a:
        a=a.split('\t')
        b=[float(i) for i in a]
        ch.append(b)
    else:
        break
print(ch)
