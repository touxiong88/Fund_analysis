#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/19 17:37
# @Author  : ‘sunhz’ 
# @Site    : 
# @File    : fund1000.py
# @Software: PyCharm Community Edition
# 基金一共有6500多只基金，我现在先取其中的1000只基金，近2年的交易数据，
# 然后用Pandas分析，大家猜猜看哪一天的买最划算
# @from https://zhuanlan.zhihu.com/p/27231711
import pandas as pd
import numpy as np

file='fund_3.1.csv'
df=pd.read_csv(file)
print len(df)
print df.head()

df=df.set_index(df['fund_id'])
print df.head()

#remove NA row
df2=df.dropna()
print 'dropna column',len(df2)

df_no_fund_name=df2.drop(['fund_name','fund_id'],axis=1)
print df_no_fund_name.head()

#del the '%',then we can sort
def clean_num_in_column(column):
    return column.apply(drop_percent_sign)

def drop_percent_sign(state):
	if state.endswith('%'):
		return float(state.replace('%',''))#一定要变成浮点数字

df_drop_percent=df_no_fund_name.apply(clean_num_in_column)

# get max item in each column ,check the max item info
def get_large_in_column(column):
	return column.sort_values(ascending=False).iloc[0]
print df_drop_percent.apply(get_large_in_column)

range=100
print df_drop_percent.sort_values(by=['from_start'],ascending=False).head(range)
fs_index=df_drop_percent.sort_values(by=['from_start'], ascending=False).head(range).index
print fs_index

#sort the funds by 'three_year'
print df_drop_percent.sort_values(by=['three_year'],ascending=False).head(range)
y3_index=df_drop_percent.sort_values(by=['three_year'],ascending=False).head(range).index

#获得 按照基金成立一年以来涨幅 大小排序
#sort the funds by 'one_year'
y1_index=df_drop_percent.sort_values(by=['one_year'],ascending=False).head(range).index

#sort the funds by 'six_month'
m6_index=df_drop_percent.sort_values(by=['six_month'],ascending=False).head(range).index

#sort the funds by the 'three_month'
m3_index=df_drop_percent.sort_values(by=['three_month'],ascending=False).head(range).index

#sort the funds by 'one_month'
m1_index=df_drop_percent.sort_values(by=['one_month'],ascending=False).head(range).index


fs_index_set=set(fs_index)
y3_index_set=set(y3_index)
y1_index_set=set(y1_index)
m6_index_set=set(m6_index)
m3_index_set=set(m3_index)
m1_index_set=set(m1_index)

#check the mix one during 6 columns
mix_6c=fs_index_set&y3_index_set&y1_index_set&m6_index_set&m3_index_set&m1_index_set
print 'mix 6c:',mix_6c

#check the mix one during 5 columns
mix_5c=y3_index_set&y1_index_set&m6_index_set&m3_index_set&m1_index_set
print 'min 5c:',mix_5c

#check the mix one during 4 columns
mix_4c=y1_index_set&m6_index_set&m3_index_set&m1_index_set
print 'mix 4c:',mix_4c

#check the detailed info aboout the mix_4c
df_drop_percent=df_drop_percent.drop(['from_start','three_year'],axis=1)
for each in mix_4c:
    fund_id=df_drop_percent[df_drop_percent.index==each].sum(axis=1).index[0]
    fund_total_rate=df_drop_percent[df_drop_percent.index==each].sum(axis=1).values[0]
    print fund_id,fund_total_rate


