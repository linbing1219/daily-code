
# -*- coding: UTF-8 -*-

import urllib2
from bs4 import BeautifulSoup
import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#根据网页数设置范围
#for k in range(1,6):
#根据网址获取网页
req = urllib2.Request('http://hz.fang.lianjia.com/loupan/pg'+str(1))

#建立csv存储文件，wb写 a+追加模式
csvfile = file('lianjia.csv', 'ab+')
writer = csv.writer(csvfile)
   #读取网页
user_agent = "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
headers = {"User-Agent": user_agent}    #请求头并非只有一个键值对,所以用字典类型
response = urllib2.urlopen(req)
the_page = response.read()
#解析网页
soup = BeautifulSoup(the_page,"lxml")
list0=[]
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
#提取楼盘名称字段
for tag in soup.find_all(name="div", attrs={"class": re.compile("resblock-desc-wrapper")}):
    ta1 = tag.find(name="a", attrs={"target": re.compile("_blank")})
    #添加城市字段
    list0.append(r"杭州")
    list1.append(ta1.string)

    #提取建筑面积字段
    ta2 = tag.find(name="div", attrs={"class": re.compile("resblock-area")})
    t2 = ta2.find(name="span")
    if t2 != None:
        list2.append(t2.string)
    else:
        list2.append(0)

    #提取在售状态字段
    ta3 = tag.find(name="span", attrs={"class": re.compile("sale-status")})
    list3.append(ta3.string)
    #提取住宅类型字段
    ta4 = tag.find(name="span", attrs={"class": re.compile("resblock-type")})
    list4.append(ta4.string)


    #提取每平米均价字段
for tag in soup.find_all(name="div", attrs={"class": re.compile("resblock-price")}):
    ta5 = tag.find(name="span", attrs={"class": re.compile("number")})
    if ta5 != None:
        list5.append(ta5.string)
    else:
        list5.append(0)
     #提取总价字段
    ta6 = tag.find(name="div", attrs={"class": re.compile("second")})
    if ta6 !=None:
        list6.append(ta6.string)
    else:
        list6.append(0)
#将提取的数据合并
data = []
for i in range(0,len(soup.find_all(name="div", attrs={"class": re.compile("resblock-desc-wrapper")}))):
    data.append((list0[i],list1[i], list2[i], list3[i], list4[i], list5[i],list6[i]))
   #将合并的数据存入csv
writer.writerows(data)
csvfile.close()
print list1
