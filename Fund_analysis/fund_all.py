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
import requests
from bs4 import BeautifulSoup
from  datetime  import  *
import csv
import pandas as pd
import time


# 1.数据的收集
def html_download(fund_id,s_date,e_date):
    url_base='http://app.finance.ifeng.com/data/fund/jjjz.php?symbol='
    data_range='&begin_day=%s&end_day=%s'%(s_date,e_date)
    url=url_base+fund_id+data_range
    print url
    try:
        response=requests.get(url)
    except Exception as e:
        print e
        return []

    response.coding='utf-8'
    soup=BeautifulSoup(response.content,'html.parser')
    print soup.title.text

    trs=soup.find_all('tr')
    return trs
# 2.数据的清洗


def get_weekday(data):
    w_day=datetime.strptime(data,'%Y-%m-%d').weekday()+1
    return w_day


def decode_html(fund_id,contents):
    datas=[]
    for tr in contents[1:]:
        fund_each_day_info=[s for s in tr.text.split('\n') if len(s) >1 ]
        data,rate,value= fund_each_day_info[0],\
                         fund_each_day_info[4].replace('%',''),\
                         fund_each_day_info[2]
        datas.append((data,float(rate),value,get_weekday(data)))
    return datas


# 3.数据的存储
def write_csv(fund_id,funds):
    head=['data','rate(%)','fund_value','weekday']
    fund_name='fund_data/fund_%s.csv'%(fund_id)
    with open(fund_name,'wb') as wf:
        writer=csv.writer(wf)
        writer.writerow(head)
        for each in funds:
            writer.writerow(each)


# 数据分析
def read_csv(fund_id):
    file='fund_%.csv'%(fund_id)
    df=pd.read_csv(file)

    # 目前我们的date是第二列，我们需要做一些数据处理，把date作为index
    # 我们用pandas非常强大的to_datetime函数
    df['date']=pd.to_datetime(df['date'])
    # 把日期作为index
    df=df.set_index('date')

    # 看一下一年有多少天是没有涨的
    df_price_decline=df[df['rate(%)']<0]
    print df_price_decline

    # 按照weekday分组，统计一周那天跌的概率最大
    # 然后排序一下
    weekday_df=df_price_decline.groupby('weekday')
    top_weekday_price_decline=weekday_df.size().sort_values(ascending=False.head(1))
    if top_weekday_price_decline >=1:
        return top_weekday_price_decline.index[0]
    else:
        retuen -1


def get_today():
    return datetime.now().strftime('%Y-%m-%d')


# 凤凰网查询期间不能超过2年
def get_years_ago(  n  ):
    time_now = datetime.now()
    time_year_ago = time_now - timedelta(365*n)
    return time_year_ago.strftime('%Y-%m-%d')


# 4.数据的分析
# 1）pandas有一个非常强大的库read_csv(file)，可以直接把csv文件转换成DataFrame数据结构
# 2）利用dataframe对数据进行处理
if  __name__ == '__main__':  # 文件运行main入口
    for i in range(338,1000):
        f_id=str(i)
        fund_id = f_id.zfill(6) # 字符串前面补0
        fund_html=html_download(fund_id,get_years_ago(2),get_today())
        time.sleep(3)
        if len(fund_html) < 10: # 无效的网址返回空list []
            continue
        fund_data=decode_html(fund_id,fund_html)
        write_csv(fund_id,fund_data)

# 嘉实基本面50[160716]
# 易方达消费行业[110022]


        # for f_data in fund_data:
    #    # datas.append((data, float(rate), value, get_weekday(data)))
    #    list1=['日期','盈亏','净值','星期']
    #    dict_fund=dict(zip(list1, fund_data))
    #     print dict_fund

    # for m in fund_data:
    #     print m
    #     dict_fund={
    #         '日期': m[0],
    #         '盈亏': m[1],
    #         '净值': m[2],
    #         '星期': m[3]
    #     }
    # for d_fund in dict_fund:
    #     print d_fund
    # for s in fund_htmls:
    #    print s#.encode('utf-8')
    # print get_weekday('2015-05-05')
# 把date作为index
    # df['date']=pd.to_datetime(df['date'])
    # df=df.set_index('date')

# 看下1年有多少天是跌的
    # df_price_decline=df[df['rate(%)']<0]


