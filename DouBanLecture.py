#!/usr/bin/env python
# coding=utf-8
import urllib
import codecs
from bs4 import BeautifulSoup
from datetime import datetime


class Activity:
    def __init__(self):
        self.title=U""
        self.eventUrl=U""
        self.tags=U""
        self.eventTime=U""
        self.eventFee=U""
        self.eventLocation=U""
        self.startDate=datetime.now()
        self.endDate=datetime.now()


    def IsBeforeThreeDays(self,curTime,startTime,daysCount):
        if(isinstance(curTime,datetime) and isinstance(startTime,datetime)):
            timeDelta = startTime-curTime
            if (timeDelta.days > daysCount):
                return True
            else:
                return False
        else:
            return False


    def IsBetween(self,curTime,startTime,endTime):
        if(isinstance(curTime,datetime) and isinstance(startTime,datetime) and isinstance(endTime,datetime)):
            toStart = curTime-startTime
            toEnd = endTime - curTime

            if( toStart.days > 0 and toEnd.days > 0):
                return True
            else:
                return False
        else:
            return False
        

    def IsContain(self,strContext):
        if(isinstance(strContext,unicode) and isinstance(self.eventLocation,unicode)):
            if(self.eventLocation.find(strContext) > -1):
                return True
            else:
                return False
        else:
            return False


    def IsUseful(self):
        curTime = datetime.now()
        if(self.IsBeforeThreeDays(curTime,self.endDate,2) or self.IsBetween(curTime,self.startDate,self.endDate)):
            if(self.IsContain(U"北京大学") or self.IsContain(U"清华大学")):
                return True
            else:
                return False
        else:
            return False
        

    def SetTitle(self,value):
        if (isinstance(value,unicode)):
            strList = value.split()
            for elem in strList:
                self.title = self.title+elem+" "


    def SetTags(self,values):
        if (isinstance(values,unicode)):
            strList = values.split()
            for elem in strList:
                self.tags = self.tags+elem+" "

    def SetEventTime(self,value):
        if (isinstance(value,unicode)):
            strList = value.split()
            for elem in strList:
                self.eventTime = self.eventTime+elem+" "

    def SetEventFee(self,value):
        if (isinstance(value,unicode)):
            strList = value.split()
            for elem in strList:
                self.eventFee = self.eventFee+elem+" "

    def SetEventLocation(self,value):
        if (isinstance(value,unicode)):
            strList = value.split()
            for elem in strList:
                self.eventLocation = self.eventLocation+elem+" "

    def SetEventUrl(self,value):
        self.eventUrl=value

    def SetStartTime(self,value):
        self.startDate=datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")
    def SetEndTime(self,value):
        self.endDate=datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")
    def __str__(self):
        strResult = U"Title"+self.title.encode('utf8')
        strResult = U"Tags:"+self.tags
        return strResult
    
    def GetStr(self):
        strResult =U""
        if (self.IsUseful()):
            strResult="**********************\n"
            strResult = strResult + U"标题:"+self.title+"\n"
            strResult = strResult + U"链接:"+self.eventUrl+"\n"
            strResult = strResult + U"标签:"+self.tags+"\n"
            strResult = strResult + U"活动时间:"+self.eventTime+"\n"
            strResult = strResult + U"费用:"+self.eventFee+"\n"
            strResult = strResult + U"活动地点:"+self.eventLocation+"\n"
            strResult = strResult + U"开始时间:"+self.startDate.strftime("%Y-%m-%d %H:%M:%S")+"\n"
            strResult = strResult + U"结束时间:"+self.endDate.strftime("%Y-%m-%d %H:%M:%S")+"\n"
        return strResult

class DouBanJiangZuo:
    def __init__(self):
        return

    def GetHtml(self,strUrl):
        context = urllib.urlopen(strUrl)        
        strHtml=context.read()
        return strHtml


    def ParseActivity(self,divElem):
        action = Activity()
        #Title
        divTitle = divElem.find_all('div',class_='title')
        if(len(divTitle) > 0 ):
            action.SetTitle(divTitle[0].text.lstrip().rstrip())
            action.SetEventUrl(divTitle[0].a['href'])

        #tags
        tagsList = divElem.find_all('p',class_='event-cate-tag hidden-xs')
        if(len(tagsList) > 0):
            action.SetTags(tagsList[0].text.lstrip().rstrip())


        #eventTime
        timeList = divElem.find_all('li',class_='event-time')
        if(len(timeList)> 0):
            action.SetEventTime(timeList[0].text.lstrip().rstrip())
            timeNode = timeList[0].time
            endTime = timeNode.find_next_sibling('time')
            action.SetStartTime(timeNode['datetime'])
            action.SetEndTime(endTime['datetime'])


        #eventLocation
        eventLocation = divElem.find_all('meta',itemprop='location')
        if (len(eventLocation) > 0):
            action.SetEventLocation(eventLocation[0]['content'])

        #eventFee
        eventFee = divElem.find_all('li',class_='fee')
        if(len(eventFee) > 0 ):
            action.SetEventFee(eventFee[0].text.lstrip().rstrip())

        #event Time
        strResult = U""+action.GetStr()
        return strResult
    def ParseHtml(self,strHtml):
        bsParse = BeautifulSoup(strHtml)
        strList = list()
        infoList = bsParse.find_all('div',class_='info')
        for elem in infoList:
            strAct = self.ParseActivity(elem)
            if(len(strAct) > 0):
                strList.append(strAct)
        return strList




util = DouBanJiangZuo()
index = 0
strBaseUrl="https://beijing.douban.com/events/week-all-128526?start=%s"

strTotal=U""
for index in range(0,40):
    strUrl = strBaseUrl%str(index*10)
    strHtml = util.GetHtml(strUrl)
    strList = util.ParseHtml(strHtml)
    for elem in strList:
        strTotal=strTotal+elem

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
user = 'xxxxxx@email.com'
pwd = 'xxxxyyy'
to = ['youmail@email.com']
msg = MIMEMultipart()
msg['Subject'] = '豆瓣大学讲座'

strTotal=strTotal+U"\n 来自Dennis的邮件\n"

content1 = MIMEText(strTotal.encode('utf8'), 'plain')
msg.attach(content1)
#-----------------------------------------------------------
s = smtplib.SMTP('smtp.qq.com')
s.login(user, pwd)
s.sendmail(user, to, msg.as_string())
print('发送成功')
s.close()

