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


#shibor发布页面
shiborUrl="http://www.shibor.org/shibor/web/html/shibor.html"
#接收shibor数据的服务器接口
#serverUrl="http://www.financedatas.com/shibor/gather/"
serverUrl="http://172.16.192.222:8080/shibor/"
#日志的文件的配置信息
logging.basicConfig(filename="/tmp/shibor.log",level=logging.DEBUG,format="%(levelname)s:%(asctime)s:%(message)s")

class Shibor(object):
    """用于shibor利率相关的数据收集"""

    def __init__(self,shiborUrl=shiborUrl,serverUrl=serverUrl):
        """"""
        #把要收集的web页面的url赋值给__shiborurl
        #打印日志
        logging.info("in  __init__ function")
        self.__shiborUrl=shiborUrl
        self.__serverUrl=serverUrl
        #打印日志
        logging.info("out __init__ function shiborUrl={0}  serverUrl={1}".format(self.__shiborUrl,self.__serverUrl))
    def extra(self):
        """把数据从html中抽取出来..."""
        logging.info("in  extra function")
        result={}
        tables=None
        #注意这个html是一个BeautifulSoup对象
        rawHtml=requests.get(self.__shiborUrl).content
        html=BeautifulSoup(rawHtml,"lxml",from_encoding='GBK')
        tables=html.body.findAll('table')
        table0=tables[0]
        #----以下为真正的数据抽逻辑
        #--  01：抽取shibor发布的时间、这个时间在第二个td中指明。
        pushdate=str(table0.findAll('tr')[1].td.getText()).replace('&nbsp;','')
        result['pushDate']=pushdate
        #--  02：抽取shibor的各个期限长度的利率信息、它们在同一个表中、但是不同的tr中对应的期限不同。
        table3=tables[3]
        trs=table3.findAll('tr')
        #--  03：O/N 隔夜利率
        oneNight=trs[0].findAll('td')[2].getText()
        result['oneNight']=oneNight
        #--  04：1W  一周期利率
        oneWeek=trs[1].findAll('td')[2].getText()
        result['oneWeek']=oneWeek
        #--  05：1W  两周期利率
        twoWeek=trs[2].findAll('td')[2].getText()
        result['twoWeek']=twoWeek
        #--  06：1M  一月期利率
        oneMonth=trs[3].findAll('td')[2].getText()
        result['oneMonth']=oneMonth
        #--  07：2M  三月期利率
        threeMonth=trs[4].findAll('td')[2].getText()
        result['threeMonth']=threeMonth
        #--  08：3M  六月期利率
        sixMonth=trs[5].findAll('td')[2].getText()
        result['sixMonth']=sixMonth
        #--  09：6M  九月期利率
        nineMonth=trs[6].findAll('td')[2].getText()
        result['nineMonth']=nineMonth
        #--  10：9M  一年期利率
        oneYear=trs[7].findAll('td')[2].getText()
        result['oneYear']=oneYear
        logging.info("out extra function")
        return result

    def format(self,data=None):
        """对抽取到的数据进行格式化
        pushDate --> datetime
        others   --> decimal
        """
        logging.info("in  format function")
        if data == None:
            result=self.extra()
        else:
            result=data
        #把pushDate 的数据由str 转换到datetime 类型.
        datestr,timestr=result['pushDate'].split(' ')
        yearint,monthint,dayint=[ int(x)for x in datestr.split('-')]
        hourint,mineteint=[int(x) for x in timestr.split(':')]
        result['pushDate']=datetime(yearint,monthint,dayint,hourint,mineteint,second=0)
        #把其它key的数据由str 转换到float
        for key in result.keys():
            if key != 'pushDate':
                result[key]=float(str(result[key]))
        logging.info("out format function {0}".format(result))
        return result

    def postto(self):
        """
        1、调用extra 完成数据的抽取
        2、调用format 完成数据的格式化
        3、通过post请求把数据上传到服务器
        """
        rawData=self.extra()
        data=self.format(data=rawData)
        response=requests.post(self.__serverUrl,data=data)
        print(response)




if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--shiborUrl',default=shiborUrl,help='shibor利率公布的页面')
    parser.add_argument('--serverUrl',default=serverUrl,help='服务器收集shibor的接口')
    args=parser.parse_args()
    shibor=Shibor(shiborUrl=args.shiborUrl,serverUrl=args.serverUrl)
    shibor.postto()
    #data=shibor.format()
    #print(data)