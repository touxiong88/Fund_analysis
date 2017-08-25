#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/23 10:39
# @Author  : ‘DIY’ 
# @Site    : 
# @File    : QuXianNiHe2.py
# @Software: PyCharm Community Edition
# http://blog.sina.com.cn/s/blog_aed5bd1d0102vid7.html

#潘海东,2014/1/13
#使用非线性最小二乘法拟合
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
#用指数形式来拟合
x = np.arange(1, 17, 1)
y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])
def func(x,a,b):
    return a*np.exp(b/x)
popt, pcov = curve_fit(func, x, y)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
yvals=func(x,a,b)
print yvals
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='curve_fit values')
plot3=plt.plot(y, yvals, 'r',label='y y values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('curve_fit')
plt.show()
plt.savefig('p2.png')