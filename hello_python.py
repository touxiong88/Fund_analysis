#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 15:26
# @Author  : ‘sunhz’ 
# @Site    : https://github.com/touxiong88
# @File    : hello_python.py
# @Software: PyCharm Community Edition

from __future__ import division
from numpy.random import randn
import numpy as np
import os
import matplotlib.pyplot as plt
np.random.seed(12345)
plt.rc('figure', figsize=(10, 6))
from pandas import Series, DataFrame
import pandas as pd
np.set_printoptions(precision=4)



df = DataFrame(np.random.randn(10, 4).cumsum(0),
               columns=['A', 'B', 'C', 'D'],
               index=np.arange(0, 100, 10))

print df

df['E']=np.random.randn(10).cumsum(0)

print df

df.plot()
plt.show()