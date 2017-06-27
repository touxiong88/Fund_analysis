#!/usr/bin/python
#encoding:utf-8

import this
import urllib
import urllib2
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context()

#() 元祖 不可修改
#[] 表示list
#{} 表示字典

def getList():
    return ["123|52"]

#软卧索引 = 23  硬卧 = 28 车次 =3 出发时间 = 8
n = 0
for i in getList():
    html = urllib.urlopen('https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-10-04&from_station=BJP&to_station=XKS').read()
    for y in i.split('|'):#分割
        y +=1
        trn = i.split('|')
        if trn[23] != '无' or  trn [23] != '--':
        	continue
        print n,y
    break

if  __name__ == '__main__': #文件运行main入口
    getList()