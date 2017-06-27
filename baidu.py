# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:26:00 2017

@author: sunhz
"""

import urllib2

request = urllib2.Request("http://www.baidu.com")
response = urllib2.urlopen(request)
print response.read()