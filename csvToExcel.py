#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 10:36
# @Author  : ‘sunhz’ 
# @Site    : 
# @File    : csvToExcel.py
# @Software: PyCharm Community Edition

#导入相应模块
import csv
import xlwt
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def csv_to_xls(filename):
    myexcel = xlwt.Workbook(encoding = 'utf-8')
    mysheet = myexcel.add_sheet("sheet1")
    csvfile = open(filename,"rb")
    reader = csv.reader(csvfile)
    l = 0
    for line in reader:
        r = 0
        for i in line:
            mysheet.write(l,r,i)
            r=r+1
        l=l+1
    excel_filename = str(filename.split(".")[0]) + ".xls"
    myexcel.save(excel_filename)
    return excel_filename


def main():
    path=r'E:\python\py27\funds'
    fname_list=[os.path.join(root,fn) for root,dirs,files in os.walk(path) for fn in files]
    print(len(fname_list))
    for fname in fname_list:
        file_name = csv_to_xls(fname)
        print file_name

if __name__ == '__main__': # 主函数入口
    main()