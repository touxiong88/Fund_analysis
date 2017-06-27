# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 10:49:21 2017
保存峰值
下降斜率阈值
各个参数权重
半年、一年历史数据波形 稳步上升
@author: sunhz
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.error
import time


filename = "D:\\Cadence\\SPB_16.5\\work\\py27\\fund.txt"

url=["http://fund.eastmoney.com/160716.html",
#     "http://fund.eastmoney.com/110022.html",
#     "http://fund.eastmoney.com/070032.html",
#     "http://fund.eastmoney.com/420003.html",
     "http://fund.eastmoney.com/519185.html"]

#wb_data=requests.get(url[0])
#soup=BeautifulSoup(wb_data.text,'lxml')
#titles=soup.select('div[12].div.div.div[1].div[1].div')
#for title in zip(titles):
#   print title

#html=urlopen(url[0]).read()#.decode('raw_unicode_escape')
#print(html)
#gz_gsz //*[@id="gz_gsz"] #body > div:nth-child(11) > div > div > dl > dd:nth-child(2) > a
#soup = BeautifulSoup(html)
#print soup.prettify()
#nameList = soup.findAll("span", {"class":"ui-font-large ui-color-red ui-num"})
#for name in nameList:
#    print(name.get_text())
    
#print(bsObj.td)
#print(html.read())

#find_re = re.compile(r'<div id="statuspzgz" class="fundpz"><span class=".+?">(.+?)</span>',re.DOTALL)
#time_re = re.compile(r'<p class="time">(.+?)</p>',re.DOTALL)
names = [];
codes = [];
values = [];
times = [];
dutys =[];        #<span class="ui-font-middle ui-color-green ui-num" id="gz_gszzl">-0.02%</span>
#body > div:nth-of-type > div > div > a:nth-of-type(7)
#//*[@id="body"]/div[12]/div/div/div[1]/div[1]/div/text()

name_re = re.compile(r'<a href="http://fund.eastmoney.com/\d*.html" target="_self">(.+?)</a>',re.DOTALL)
Fundcd_re = re.compile(r'http://fund.eastmoney.com/(.+?).html',re.DOTALL)
value_re = re.compile(r'span class="ui-font-large ui-color-red ui-num" id=".+?">(.+?)</span>',re.DOTALL)
time_re = re.compile(r'<span id="gz_gztime">(.+?)</span>',re.DOTALL)
duty_re = re.compile(r'<span class="ui-font-middle ui-color-green ui-num" id="gz_gszzl">(.+?)</span>',re.DOTALL)

for ul in url:   
    html=urlopen(ul).read()#.decode('utf-8','ignore')
    time.sleep(2)
    names.append(str(name_re.findall(html)))
    codes.append(str(Fundcd_re.findall(ul)))
    values.append(str(value_re.findall(html)))
    dutys.append(str(duty_re.findall(html)))
    times.append(str(time_re.findall(html)))
    
    #fund_data = {
     #       "名称: ":str(name_re.findall(html)).decode('string_escape'),
     #       "代码：": str(Fundcd_re.findall(ul)),
     #       "净值：": str(value_re.findall(html)),
     #       "更新时间：": str(time_re.findall(html))  
     #       }
    #print "名称: " + str(name_re.findall(html)).decode('string_escape')
    #print "代码：" + str(Fundcd_re.findall(ul))
    #print "净值：" + str(value_re.findall(html))        
    #print "更新时间：" + str(time_re.findall(html))  
    #print ''
print (dutys    )
print("  基金名称   基金代码     当日净值    增幅       日期    最高净值  购买盈亏  购买增幅  购买时长")
for (name, code, value, duty, t_time) in zip(names, codes, values, dutys, times):
    print (name.decode('string_escape')),
    print (code),
    print (value),
    print (duty),
    print (t_time)
    
fund_data ={
        'd_name':names,
        }
# dict((names,codes,values,times))
with open(filename, 'w') as f:
    f.write(str(fund_data).decode('string_escape'))
    
