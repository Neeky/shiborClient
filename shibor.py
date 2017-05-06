#/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个shiber.py 用于收集上海银行间同业折放利率
"""
import json
import requests
import BeautifulSoup as bs
from datetime import datetime

shiborUrl="http://www.shibor.org//shibor/web/html/shibor.html"



class Shibor(object):
    """用于shibor利率相关的数据收集"""

    def __init__(self,shiborurl=shiborUrl):
        """"""
        #把要收集的web页面的url赋值给__shiborurl
        self.__shiborurl=shiborurl
        #得到返回的http内容
        self.__html=requests.get(self.__shiborurl).content
        #把http内容包装成bs对象、用于后面的操作
        self.html=bs.BeautifulSoup(self.__html)

    def extra(self):
        """把数据从html中抽取出来..."""
        result={}
        #注意这个html是一个BeautifulSoup对象
        html=self.html
        tables=self.html.body.findAll('table')
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


        return result
        
    


if __name__=="__main__":
    shibor=Shibor()
    data=shibor.extra()
    print(data)