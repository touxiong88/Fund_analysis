# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:26:00 2017

@author: sunhz
# 爬取天天基金排行rank
http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2016-11-13&ed=2017-11-13&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.803325651389825%22
"""
import urllib2
import re, csv,os
from  datetime import *

# 确保文件编码格式为 utf-8 如果此文件以前编码不是utf-8 则转为utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

CSV_File = 'fund_data/fund100.csv'  # 基金排名前100名


# 1.数据的收集
def html_download(page, s_date, e_date):

    url_base = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd='
    url_middle = '%s&ed=%s'%(s_date, e_date)
    url_page = '&qdii=&tabSubtype=,,,,,&pi=%s'%(page)
    url_end = '&pn=50&dx=1&v=0.803325651389825%22'
    url = url_base + url_middle + url_page + url_end
    print url
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except Exception as e:
        print e
        return []

    return response.read()


def get_today():
    return datetime.now().strftime('%Y-%m-%d')


# 天天基金不能超过2年
def get_years_ago(n):
    time_now = datetime.now()
    time_year_ago = time_now - timedelta(365 * n)
    return time_year_ago.strftime('%Y-%m-%d')

# 2.数据的清洗存储
def write_csv(fund_text):
    fund_page = fund_text[24:-150]  # 掐头去尾
    # 以 "," 作为分割
    items = re.split('","', fund_page)
    # 按行写入csv文件
    # print type(items) # 打印数据类型
    with open(CSV_File, 'ab') as f:  #ab wb
        for item in items:
            line = ''.join(item) + '\n'
            f.write(line)   # 将list按行写入csv 文件

# 3.数据显示
def rank_my_fund(my_funds):
    rank = 0;
    with open(CSV_File,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rank = rank + 1
            for my_fund in my_funds:
                if(row[1] == my_fund):
                    print '周排名',rank,my_fund
                    break



if __name__ == '__main__':  # 文件运行main入口
    print "hello python"
    my_funds = ['华安动态灵活配置', '兴全沪深300指数(LOF)', '华安宏利混合', '嘉实前沿科技沪港深股票',
                '东方红产业升级混合', '汇添富成长焦点混合', '银华中小盘混合',
                '建信基本面60联接','兴全社会责任混合'] #天天基金不支持 todo

    os.remove(CSV_File) #清除旧数据
    for page in range(1, 50): #2017-11-14  共计 74页
        fund_text = html_download(page, get_years_ago(1), get_today())
        write_csv(fund_text)
    rank_my_fund(my_funds) #显示我的基金排名

        # 嘉实基本面50[160716]
        # 兴全沪深300指数(LOF)(163407)
        # 长信量化先锋混合 519983
        # 易方达消费行业[110022]
        # 3年 1年 6个月 3个月 1个月 都在涨的基金
        # 150050 000619 150124 110022
        # 易方达供给改革混合 002910
        # 中融国证钢铁	 168203

        # 借道基金  -- 排除
        # 164906 交银中证海外 513050 易方达中概互联
        # 000988 嘉实全球互联 001668 汇添富全球互联
