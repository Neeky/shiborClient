#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
这个shiber.py 用于收集上海银行间同业折放利率
python 版本 python-3.x
"""


import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import logging
import string

#接收shibor的服务接口
serverUrl="http://172.16.192.222:8080/shibor/"



if __name__=="__main__":
    parser=argparse.ArgumentParser()
    #接收shibor数据的接口
    parser.add_argument('--serverUrl',default=serverUrl,help='服务器收集shibor的接口')
    #shibor相关数据所在的文件名(这里只是一个前缀)
    parser.add_argument('--file',default=r"/Users/jianglexing/Downloads/Shibor数据",help='shibor利率的历史记录文件')
    #默认从哪个年份开始加载数据
    parser.add_argument('--from',default=2006)
    #默认加载到哪个年份为止
    parser.add_argument('--to',default=2017)
    args=parser.parse_args()
    #年份列表
    fileNames=[2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
    #第一步：拼接出真正的数据文件名
    fileNames=["{0}{1}.txt".format(args.file,item) for item in fileNames]
    
    try:
        #对文件进行解析
        lines=None
        for fileName in fileNames:
            print("{0}  {1}".format("-"*8,fileName))
            with open(fileName,encoding='GBK') as fh:
                #lines 表示数据行
                lines=[line for line in fh][2:]
            #为第行数据单独做处理、并发往serverURL
            for line in lines:
                print("{0}  {1}".format("-"*8,line))
                #数据处理
                line=line.replace('      ',',')
                line=line.replace('     ',',')
                datas=line.split(',')[:-1]
                #针对时间(pushDate)做处理2000-01-01 --> 2000-01-01 11:00
                year,month,day=datas[0].split('-')
                pushDate=datetime(year=int(year),month=int(month),day=int(day),hour=11)
                #包装post时的数据
                data={}
                data['pushDate']=pushDate
                data['oneNight']=datas[1]
                data['oneWeek']=datas[2]
                data['twoWeek']=datas[3]
                data['oneMonth']=datas[4]
                data['threeMonth']=datas[5]
                data['sixMonth']=datas[6]
                data['nineMonth']=datas[7]
                data['oneYear']=datas[8]
                #post数据
                requests.post(serverUrl,data)
    except Exception as e:
        print(e)