# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 14:06:35 2017
http://www.dataguru.cn/thread-64424-1-1.html
@author: sunhz
"""

# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import urllib2

# 单位净值      asset-value     0.9360
# 净值增长率    asset-amt       1.08%
# 累计净值      asset-all       0.9360
# 净值更新日期  date            2013/2/5          
# 最近估值      price
# 涨跌幅        amt
# 涨跌额        amt-value
# 最新规模      scale           13.68亿元
# 风险等级      risk            高风险
# 申购状态      subscribe-status 可申购
# 赎回状态      redeem-status   可赎回

value_list = ["asset-value", "asset-amt", "asset-all", "date", "price", "amt", "amt-vaue", "scale", "risk", "subscribe-status","redeem-status"]

class FundDataParser(HTMLParser):
    def __init__(self, value_list = value_list):
        HTMLParser.__init__(self) # old-style class could not use super 
        self._process = False
        self.value_list =  value_list
        self.attr = ""
        self.data = {}
        self.result = {}
        
    def get(self, code):
        url = "http://finance.sina.com.cn/fund/quotes/%s/bc.shtml" % (code)
        f = urllib2.urlopen(url)
        html = unicode(f.read(),"utf-8")
        self.feed(html)
        self.close()
        self.result = self.data
        self.data = {}
        return(self.result)
                
    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for attr in attrs:
                if (attr[0] == "class"):
                    # case <span class="asset-amt red">
                    for attr_name in attr[1].split():
                        if attr_name in self.value_list:
                            self._process = True
                            self.attr = attr_name
                    
    def handle_data(self, data):
        if self._process:
            self.data[self.attr] = data
            self._process = False

def main():
    """docstring for main"""
    parser = FundDataParser()
    #print parser.get("040020")
    print parser.get("213008")
    
if __name__ == '__main__':
    main()