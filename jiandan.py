# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 16:33:11 2017
http://v.youku.com/v_show/id_XMjc2OTI4MzMxNg==.html?from=s1.8-1-1.2&spm=a2h0k.8191407.0.0
@author: sunhz
"""

from urllib2 import urlopen
import re

url = 'http://jandan.net/duan'

req = urlopen(url)
html = req.read()
html_str = html.decode('utf-8')

pattern = re.compile('<p>.*</p>')
groups = pattern.findall(html_str)

print(groups)

a={2,5,2,3,0,4}
b=5
for b in a:
    print(b)
    b += 1;