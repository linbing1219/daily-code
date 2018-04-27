
# -*- coding: UTF-8 -*-

import urllib2
from bs4 import BeautifulSoup
import csv
import re
import sys
import os
import time
from price_data import BaseData
from price_data import PrireData

reload(sys)
sys.setdefaultencoding('utf-8')

FILE_DIR = os.path.dirname(__file__)

def result_html(base_data_list, price_data_list):
    body = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>杭州房价</title>
    </head>>
    '''
    body += '\n' + r'<h2><span style="color: #339966;"><font face="STKaiti">杭州最新可上车的房源（数据来自链家）  获取时间：' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +'</font></span></h2>'
    body += '\n' + r'<table border="1" class="gridtable" id="table">'
    body += '\n' + r'<tbody>'
    body += '\n' + r'<tr align="center" style="color:green;font-family: Arial;">'
    body += '\n' + r'<th nowrap="nowrap"><font face="Arial">序号</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">区域</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">楼盘名称</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">楼盘地址</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">面积</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">销售状态</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">楼盘类型</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">单价</font></th>' \
                   r'<th nowrap="nowrap"><font face="Arial">总价</font></th>'
    for i in range(0, len(base_data_list)):
        if base_data_list[i].get_type() != "住宅":
            continue
        if base_data_list[i].get_status() == "售罄":
            continue
        nrow = '\n' + r'<tr align="center">'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + str(i) + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_location() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_house_name() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_address() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_area() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_status() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + base_data_list[i].get_type() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + price_data_list[i].get_unit_price() + r'</font></td>'
        nrow += r'<td nowrap="nowrap"><font face="Arial">' + price_data_list[i].get_total_price() + r'</font></td>'
        body += nrow
    body += '\n' + r'</td></tr></tbody></table>'

    html_file = os.path.join(FILE_DIR, "../../django-code/web/templates", "fangjia.html")

    f = open(html_file, "w")
    f.write(body)
    f.close()
    pass

def main():
    #根据网页数设置范围
    base_data_list = []
    price_data_list = []
    for k in range(1,60):
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
            _location = tag.find(name="div", attrs={"class": re.compile("resblock-location")})
            _house_name = tag.find(name="a", attrs={"target": re.compile("_blank")})
            # 添加区域字段
            location = _location.find(name="span").string
            address = _location.find(name="a", attrs={"target": re.compile("_blank")}).string
            house_name = _house_name.string

            #提取建筑面积字段
            resblock_area = tag.find(name="div", attrs={"class": re.compile("resblock-area")})
            _resblock_area = resblock_area.find(name="span")
            if _resblock_area.string != None:
                area = _resblock_area.string
            else:
                area = "未知"

            #提取在售状态字段
            sale_status = tag.find(name="span", attrs={"class": re.compile("sale-status")})
            status = sale_status.string
            #提取住宅类型字段
            resblock_type = tag.find(name="span", attrs={"class": re.compile("resblock-type")})
            type = resblock_type.string

            base_data = BaseData(location, house_name, address, area, status, type)
            base_data_list.append(base_data)

        #提取每平米均价字段
        for tag in soup.find_all(name="div", attrs={"class": re.compile("resblock-price")}):
            resblock_price = tag.find(name="span", attrs={"class": re.compile("number")})
            if resblock_price != None:
                unit_price = resblock_price.string
            else:
                unit_price = "未知"
             #提取总价字段
            second = tag.find(name="div", attrs={"class": re.compile("second")})
            if second !=None:
                total_price = second.string
            else:
                total_price = "未知"

            price_data = PrireData(unit_price, total_price)
            price_data_list.append(price_data)

        print "finish get page %s data..." % str(k)
    # 展示数据
    result_html(base_data_list, price_data_list)



if __name__ == "__main__":
    main()