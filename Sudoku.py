#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/19 15:04
# @Author  : ‘sunhz’
# @Site    :
# @File    : head.py
# @Software: PyCharm Community Edition

import itertools
import numpy as np

nums=[x for x in range(1,10)]
sequence_3nums=[p for p in itertools.permutations(nums,3) if sum(p)== 15]
print len(sequence_3nums)

for row1 in sequence_3nums:
    for row2 in sequence_3nums:
        for row3 in sequence_3nums:
            np_array_3d=np.array([row1,row2,row3])
            if sum(np_array_3d[:,0]) ==15\
                and sum(np_array_3d[:,1])==15\
                and np_array_3d.trace()==15\
                and np_array_3d[0,2]+np_array_3d[1,1]+np_array_3d[2,0]==15:
                    if len(set(np_array_3d[0]) & set(np_array_3d[1])):
                        print np_array_3d