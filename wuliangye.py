#!/usr/bin/python
#encoding:utf-8

# https://mp.weixin.qq.com/s/uPKSkYN1qbww1Jbhuqz3JA
import csv

with open('contacts.csv','rb') as f:
    reader = csv.reader(f)

#    header = reader.next()
#    print header

#    for row in reader:
#        print row

# 在上面的代码中row回事一个元祖，因此为了访问某个字段，你需要使用下表f访问，
# 而且要注意这个返回的reader是一个迭代器，迭代器只能用next或者for循环来处理

#with open('contacts.csv','rb') as rf:
#    reader = csv.DialectReader(rf)
#    for row_dict in reader:
#        print row_dict

# csv里面的 DictReader函数可以把文件读成字典列表，通过for循环吧每一行都读
# 出来每一行其实都市一个字典，可以根据key，value灵活处理


# 写入CSV文件
something = '我爱，你老婆'
with open('some.csv','wb') as wf:
    writer = csv.writer(wf)#.encodeing('utf-8')
    writer.writerows(something)

# 注意读写的时候最好按照二进制(b)的方式。因为跨平台转换的时候，有一些字符会变，
# 特别像是/n，我们称为换行符，‘0x0A’，到了Win平台会编程两个字符‘0x0D’‘0x0A’
# 所以无论读写最好都加上一个b，原样读取比较保险，可以表面一些不必要的麻烦


# 读取五粮液股票二十年的数据
# 雅虎网站上有一些县城的股票代码的csv，我们只需要去获取一下这些数据download下来
# 就可以分析了

# 处理过程如下：
# 1.首先用urllib模块里面urlretrieve抓取五粮液股票的csv文件，并down到本地
# 2，然后读取文件
# 3,可以用next读取第一行，可就是股票文件里面的头部信息

import urllib
import csv
import urllib2,cookielib



url = 'http://table.finance.yahoo.com/table.csv?s=000858.sz'
url ='http://q.stock.sohu.com/hisHq?code=cn_000001&start=20000504&end=20151215&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&r=0.8391495715053367&0.9677250558488026'

print urllib.urlretrieve(url,'WuLiangYe.csv')

with open('WuLiangYe.csv','rb') as rf:
    read_csv = csv.reader(rf)

    header = read_csv.next()
    #print header

#    row = read_csv.next()
#    print row


# 4.萃取股票成交量超过2亿元的数据，并写到新文件
# 获取二十年来的股票成交量超过2亿元，然后写到一个新的CVS文件里

# 处理过程如下 ：
# 1.我妈先从csv文件中读取
# 2.把头部信息取出来
# 3.创建一个写文件的句柄，然后创建一个写CSV的句柄
# 4.循环处理每一行，当每一行的第6想(成交量)大于1亿元时，把这一行写入新的CSV文件
    with open('new_WuLiangYe.csv','wb') as wf:
        writer_csv=csv.writer(wf)
        writer_csv.writerow(header)

        for row in read_csv:
            if int(row[5]) >= 500000000:
                writer_csv.writerow(row)

# 注意row[5]是股票的成交量，是一个字符串要转为int，不然没法比较，发现20年里只有
# 2天是成交量超过2亿元的

# 5.获取五粮液近20年的最高价格和对应的日期
# 1）urllib网上下载csv文件
# 2）把csv文件读出来放到read_csv句柄
# 3）数据清洗，去掉头部，迭代器转成李彪，并把日期和股票构造出字典
# 4）字典循环一下，获取最高价和对应的日期

with open('WuLiangYe.csv', 'rb') as rf:
    read_csv=csv.reader(rf)
    stock_dict={row[0]:float(row[4]) for row in list(read_csv)[1:]}
    high_price=max(stock_dict.values())
    low_price=min(stock_dict.values())

    for k,v in stock_dict.items():
        if v==high_price:
            print k,v
        if v==low_price:
            print k,v

# 用推导列表快速生成字典，然后用max获取最高价，大家发现只需要机型就能搞定，如果用java
# c++需要复杂的多，python是不是非常高效


# python的数据分析是最最强大的地方也是我个人认为最有魅力的地方，这里只是倾听点水，真正
# 的股票数据哇局需要更复杂的建模，并且用神器pandas处理，再用matplotlib图形显示结果，



