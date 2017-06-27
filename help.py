# -*- coding: utf-8 -*-
"""
Created on Mon May 08 10:47:10 2017

@author: sunhz
"""

import this
import os

os.system('clear')
yuanzu=(1,)
print yuanzu

a = None

if  not a:
    print a
if a is not None:
    print a,'not'
    
help('oss')    
help('os.getenv')  
a = 3
b = 5
a, b = b, a
print a,b