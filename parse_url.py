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
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
import re,requests,csv,os,threading,time
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

CSV_File= 'fund3.1.csv'
lock=threading.Lock()

class Url_Download():
    def __init__(self,url):
        self.url=url
        self.funds=[]

    def cost_time(self,):
        def wrap(self):
            start=time.time()

    def html_download(self,url):
        if url is None:
            return None

        try:
            response = requests.get(url)
        except Exception as e:
            print "open the url failed,error :{}".format(e)
            return None

        if response.status_code != 200:
            return None
        return response.content


    def html_extract_content(self,html_cont):
        funds_text=[]
        if html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='gb18030')

        '''
        get all the fund id 
        '''
        title_node=soup.title
        print title_node.getText()

        uls=soup.find_all('ul',class_='num_right')
        for ul in uls:
            for each in ul.find_all('li'):
                # print each
                li_list = each.find_all('a')
                fund_info_dict={'fund_id':'',
                                'fund_name':'',
                                'fund_url':''}
                if len(li_list)>1:
                    fund=li_list[0].text
                    fund_id=re.findall(r'\d+',fund)[0]
                    fund_url=li_list[0].attrs['href']
                    fund_name=fund.decode('utf-8')[fund.find(ur'）') + 1:].encode('utf8')
                    fund_info_dict['fund_id']=fund_id
                    fund_info_dict['fund_name']=fund_name
                    fund_info_dict['fund_url']=fund_url
                    funds_text.append(fund_info_dict)

        return funds_text

    def get_all_funds_dict(self):
        text = self.html_download(self.url)
        if text:
            self.funds = self.html_extract_content(text)

        return self.funds


class Handle_Url(Thread):
    All_Funds = []
    def __init__(self,queue):
        super(Handle_Url, self).__init__()
        self.queue=queue

    @staticmethod
    def del_csv_file():
        file_path = os.path.join(os.getcwd(), CSV_File)
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def write_csv_head():
        Handle_Url.del_csv_file()
        with open(CSV_File, 'ab') as wf:
            head = ['fund_id', 'fund_name', 'one_month',
                    'three_month', 'six_month', 'one_year',
                    'three_year', 'from_start']

            writer = csv.writer(wf)
            writer.writerow(head)

    def run(self):
        print 'run in Parse_url'
        while True:
            if self.queue.empty():
                break
            else:
                fund=self.queue.get()
                url=fund['fund_url']
                fund_id=fund['fund_id']
                fund_name=fund['fund_name']
                print self.name+":"+"Begin parse :[%s %s] now"%(fund_id,fund_name)
                fund_data=self.parse_url(url)
                fund_data.insert(0,fund_id)
                fund_data.insert(1,fund_name)

                lock.acquire()
                try:
                    self.write_each_row_in_csv(fund_data)
                finally:
                    lock.release()

    def write_each_row_in_csv(self,text):
        with open(CSV_File, 'ab') as wf:
            writer=csv.writer(wf)

            writer.writerow(text)

    def html_download(self,url):
        if url is None:
            return None

        try:
            response = requests.get(url)
        except Exception as e:
            print "open the url failed,error :{}".format(e)
            return None

        if response.status_code != 200:
            return None
        return response.content

    def html_decode(self,html_cont):
        '''
        get the fund data: such as:
        [u'-0.51%', u'116.08%', u'118.93%', u'102.2%', u'118.48%', u'116.30%'] 
        '''
        fund_data=[]
        if html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='gb18030')
        #find div
        data_of_fund = soup.find_all('div', class_="dataOfFund")
        if data_of_fund:
            #get the last div
            data_itmes=data_of_fund[-1].find_all('dd',class_=None)
            if not data_itmes:
                print '!!{} No data find'.format(soup.title)
            for each in data_itmes:
                spans=each.find_all('span')
                date=spans[0].text
                rate=spans[1].text
                fund_data.append(rate)
        return fund_data

    def parse_url(self,url):
        re_sorted_fund_data=[]
        html_content=self.html_download(url)
        fund_data=self.html_decode(html_content)
        '''sort the data as:
        one_month,three_month,six_month,one_year,three_yar,start_from
        '''
        if len(fund_data)>=6:
            re_sorted_fund_data=[fund_data[0],fund_data[2],
                                 fund_data[4],fund_data[1],
                                 fund_data[3],fund_data[5]]
            return re_sorted_fund_data
        else :
            return fund_data


if __name__=='__main__':
    start=time.time()
    url_base='http://fund.eastmoney.com/allfund.html#0'

    url_download=Url_Download(url_base)
    funds=url_download.get_all_funds_dict()

    queue=Queue()
    threads=[]

    Handle_Url.write_csv_head()

    #put all the fund_text info queue
    for fund_text in funds:
        queue.put(fund_text)

    #create the multi-thread
    for i in range(8):
        c=Handle_Url(queue)
        threads.append(c)
        c.start()
    #wait for all thread finish
    for t in threads:
        t.join()

    print 'Cost:{0} seconds'.format(time.time()-start)