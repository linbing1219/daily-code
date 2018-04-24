
# -*- coding: UTF-8 -*-

import urllib2
from bs4 import BeautifulSoup
import csv
import re
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

FILE_DIR = os.path.dirname(__file__)

def result_html(list0, list1, list2, list3, list4, list5, list6):
    body = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>杭州房价</title>
    </head>>
    '''
    body += '\n' + r'<h2><span style="color: #339966;"><font face="STKaiti">杭州最新房价（数据来自链家）</font></span></h2>'
    body += '\n' + r'<table border="1" class="gridtable" id="table">'
    body += '\n' + r'<tbody>'
    body += '\n' + r'<tr align="center" style="color:green;font-family: Arial;">'
    body += '\n' + r'<th nowrap="nowrap"><font face="Arial">区域</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">楼盘名称</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">面积</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">销售状态</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">楼盘类型</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">单价</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">总价</font></th>'
    for i in range(0, len(list0)):
        nrow = '\n' + r'<tr align="center">'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list0[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list1[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list2[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list3[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list4[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list5[i] + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + list6[i] + r'</font></td>'
        body += nrow
    body += '\n' + r'</td></tr></tbody></table>'

    html_file = os.path.join(FILE_DIR, "../../django-code/web/templates", "fangjia.html")

    f = open(html_file, "w")
    f.write(body)
    f.close()
    pass

def main():
    #根据网页数设置范围
    list0 = []
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    # 建立csv存储文件，wb写 a+追加模式
    csvfile = file('lianjia.csv', 'wb')
    writer = csv.writer(csvfile)
    for k in range(1,10):
        print "begin get page %s data..." % str(k)
        #根据网址获取网页
        req = urllib2.Request('http://hz.fang.lianjia.com/loupan/pg'+str(k))
           #读取网页
        user_agent = "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        headers = {"User-Agent": user_agent}    #请求头并非只有一个键值对,所以用字典类型
        response = urllib2.urlopen(req)
        the_page = response.read()
        #解析网页
        soup = BeautifulSoup(the_page,"lxml")
        #提取楼盘名称字段
        for tag in soup.find_all(name="div", attrs={"class": re.compile("resblock-desc-wrapper")}):
            ta0 = tag.find(name="div", attrs={"class": re.compile("resblock-location")})
            ta1 = tag.find(name="a", attrs={"target": re.compile("_blank")})
            t0 = ta0.find(name="span")
            #添加城市字段
            list0.append(t0.string)
            list1.append(ta1.string)

            #提取建筑面积字段
            ta2 = tag.find(name="div", attrs={"class": re.compile("resblock-area")})
            t2 = ta2.find(name="span")
            if t2.string != None:
                list2.append(t2.string)
            else:
                list2.append("0")

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
                list5.append("0")
             #提取总价字段
            ta6 = tag.find(name="div", attrs={"class": re.compile("second")})
            if ta6 !=None:
                list6.append(ta6.string)
            else:
                list6.append("0")
        print "finish get page %s data..." % str(k)
    # 将提取的数据合并
    data = []
    print len(list0)
    for i in range(0, len(list0)):
        data.append((list0[i], list1[i], list2[i], list3[i], list4[i], list5[i], list6[i]))
        # 将合并的数据存入csv
    writer.writerows(data)
    csvfile.close()
    html_str = result_html(list0, list1, list2, list3, list4, list5, list6)



if __name__ == "__main__":
    main()