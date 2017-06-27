# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 09:24:21 2017

@author: sunhz
"""

from bs4 import BeautifulSoup
import requests
import time

url = 'https://knewone.com/discover'

def get_page(url, data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    imgs = soup.select('a.cover-inner > img')
    titles = soup.select('section.content > h4 > a')
    links = soup.select('section.content > h4 > a')
    #wrapper > div > section > div:nth-child(1) > div.hits_group-things.clearfix > article:nth-child(4) > section > h4 > a
    #//*[@id="wrapper"]/div/section/div[1]/div[1]/article[3]/section/h4/a
    for img, title, link in zip(imgs,titles,links) :
        data = {
            img.get('src'),
            title.get('title'),
            link.get('href'),
        }
        print(data)
  
def get_more_pages(start, end):
    for num in range(start, end):
        get_page(url,str(num))
        time.sleep(2)
        
        
#if __name__ == "__main__":        
    #get_more_pages(1,10)        
for i in range(1,10):
    print(i)
    
    