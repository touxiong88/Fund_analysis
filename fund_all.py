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
from pandas import Series, DataFrame
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker
# 解决 matplotlib 画图中文显示小方块
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 确保文件编码格式为 utf-8 如果此文件以前编码不是utf-8 则转为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    fund_name='fund_title/fund_%s.csv'%(fund_id)
    with open(fund_name,'wb') as wf:
        writer=csv.writer(wf)
        writer.writerow(head) # 使用 np.loadtxt需要每列数据格式一样
        for each in funds:
            writer.writerow(each)

temp_inc = 0
def get_inc(s):
    global  temp_inc
    if s >=0:
        temp_inc = s
    return temp_inc



temp_dec = 0
def get_dec(s):
    global  temp_dec
    if s <=0:
        temp_dec =-s
    return temp_dec


# 数据分析 str fund_id
def analyze_one_fund(fund_id, retuen=None):
    file='fund_title/fund_%s.csv'%(fund_id)
    # df=pd.DataFrame.from_csv(file, parse_dates=False)
    # df['fund_value'].plot()
    # plt.show()

    df=pd.read_csv(file)
    # 目前我们的date是第二列，我们需要做一些数据处理，把date作为index
    # 我们用pandas非常强大的to_datetime函数
    df['data']=pd.to_datetime(df['data'])
    # 把日期作为index
    df=df.set_index('data')
    df['inc']=[get_inc(x) for x in df['rate(%)']]
    df['dec']=[get_dec(x) for x in df['rate(%)']]
    #frames=[df['dec'],df['inc']] #dataframe 合并
    #df_new=pd.concat(frames) #dataframe 合并
    df['inc'][:60].plot()
    df['dec'][:60].plot()
    plt.title('基金_%s'%(fund_id))
    plt.plot(label=u'涨幅曲线')
    plt.xlabel('time')
    plt.ylabel('rate%')
    plt.show()

    print df

    # 看一下一年有多少天是没有涨的
    df_price_decline=df[df['rate(%)']<0]
    df_price_incline=df[df['rate(%)']>0]
    #print df_price_decline
    #print df_price_incline
    # 按照weekday分组，统计一周那天跌的概率最大
    # 然后排序一下
    weekday_df=df_price_decline.groupby('weekday')
    #print df['rate(%)'].tolist()
    #print df.index.tolist()

    top_weekday_price_decline=weekday_df.size().sort_values(ascending=False).head(1)
    if top_weekday_price_decline.size >=1:
        return top_weekday_price_decline.index[0]
    else:
        print "error"
        retuen


def get_today():
    return datetime.now().strftime('%Y-%m-%d')


# 凤凰网查询期间不能超过2年
def get_years_ago(  n  ):
    time_now = datetime.now()
    time_year_ago = time_now - timedelta(365*n)
    return time_year_ago.strftime('%Y-%m-%d')

def download_littlt_fund(begin,end):    # 下载多只基金数据
     for i in range(begin,end): # 基金号从begin end
        f_id=str(i)
        fund_id = f_id.zfill(6) # 字符串前面补0
        fund_html=html_download(fund_id,get_years_ago(2),get_today())
        # time.sleep(3)
        if len(fund_html) < 10: # 无效的网址返回空list []
            continue
        fund_data=decode_html(fund_id,fund_html)
        write_csv(fund_id,fund_data)


def download_mutiple_fund():    # 下载多只基金数据
    with open('funds/fund_3.1.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        funds_id = [row['fund_id'] for row in reader] #读 标题fund_id 的这一列
        for fund_id in funds_id:
            fund_html=html_download(fund_id,get_years_ago(2),get_today())
            # time.sleep(3)
            if len(fund_html) < 10: # 无效的网址返回空list []
                continue
            fund_data=decode_html(fund_id,fund_html)
            write_csv(fund_id,fund_data)


# 传入参数 str fund_id
def show_fund(fund_id):
    import pandas as pd
    import numpy as np
    import pylab as pl
    import matplotlib.dates as dt
    from numpy import dtype
    # from numpy import datetime64
    x = np.loadtxt(r'fund_data/fund_%s.csv'%(fund_id), delimiter=',', usecols=(0,), dtype='datetime64[D]') # 需要保证每列数据格式一样
    y = np.loadtxt(r'fund_data/fund_%s.csv'%(fund_id), delimiter=',', usecols=(1,), dtype='str')

    pl.title('基金_%s'%(fund_id))
    pl.plot(x, y,label=u'涨幅曲线')
    pl.xlabel('time')
    pl.ylabel('price')
    # pl.xlim(0.0,2016-07-06)
    # pl.ylim(8000,10000)
    pl.show()


# 传入参数 str fund_id
def run_variance(fund_id): # 计算盈亏率方差 用于评估股票波动
    # with open('fund_data/fund_%s.csv'%(fund_id), 'rb') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     nlist = [row[0] for row in reader] #读 第0列
    cnt = 0
    nlist = []
    with open('fund_data/fund_%s.csv'%(fund_id), 'rb') as csvfile:
        for i in csvfile.readlines():
            tmp = float(i.split(',')[1])
            nlist.append(tmp)
            cnt +=1

    narray = np.array(nlist)
    print narray
    sum1 = narray.sum()
    narray2 = narray * narray
    sum2 = narray2.sum()
    mean = sum1 / cnt
    variance = sum2 / cnt - mean ** 2
    print "variance: %f"%(variance)

# 4.数据的分析
# 1）pandas有一个非常强大的库read_csv(file)，可以直接把csv文件转换成DataFrame数据结构
# 2）利用dataframe对数据进行处理
if  __name__ == '__main__':  # 文件运行main入口
    print "hello python"
    #download_mutiple_fund() #下载所有只基金
    #download_littlt_fund(160716,160716+1)
    weekday=analyze_one_fund('160716') #返回周几降的概率大，适合买入
    print"decrease day is week  "+str(weekday)
    #show_fund('160716')
    #run_variance('110022')




# 嘉实基本面50[160716]
# 易方达消费行业[110022]


