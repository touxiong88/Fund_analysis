#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 10:06
# @Author  : ‘sunhz’ 
# @Site    : 
# @File    : girl.py
# @Software: PyCharm Community Edition
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 确保文件编码格式为 utf-8 如果此文件以前编码不是utf-8 则转为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys
import math
import time

def frange(start, end, step=1.0):
    if step > 0:
        while start < end:
            yield start
            start += step
    elif step < 0:
        while start > end:
            yield start
            start += step
    else:
        raise ValueError('range() step must not be zero')

def f(x, y, z):
    a = x*x + 9.0/4*y*y + z*z - 1
    return a*a*a - x*x*z*z*z - 9.0/80*y*y*z*z*z

def h(x, z):
    for y in frange(1.0, 0.0, -0.001):
        if f(x, y, z) <= 0:
            return y
    return 0.0

def writefrang():
    for z in frange(1.5, -1.5, -0.1):
        for x in frange(-1.5, 1.5, 0.05):
            v = f(x, 0, z)
            if v <= 0:
                y0 = h(x, z)
                ny = 0.01
                nx = h(x + ny, z) - y0
                nz = h(x, z + ny) - y0
                nd = 1.0/math.sqrt(nx*nx+ny*ny+nz*nz)
                d = (nx + ny - nz)*nd*0.5 + 0.5
                sys.stdout.write('.:-=+*#%@'[int(d*5)])
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def writefrange1():
    for y in frange(1.5, -1.5, -0.1):
        for x in frange(-1.5, 1.5, 0.05):
            z = x*x + y*y - 1
            f = z*z*z - x*x*y*y*y
            if f <= 0:
                sys.stdout.write('*')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def start():
    print "*"*80
def dee():
    print "-"*80
myfile=open("word.txt","rb+")
line=myfile.readlines()
for i in range(0,13):
    print line[i]
    time.sleep(3)
dee()
writefrange1()
#writefrang()
dee()
for i in range(13,174):
    print line[i]
    dee()
    i+=2
    time.sleep(2)
myfile.close()
writefrang()