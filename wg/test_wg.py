# -*- coding: utf-8 -*-
import csv
import requests
import re
import codecs


def get_infor(starturl):
    r=re.sub(r'0.html','',starturl)
    s='js/productInfo.js'
    url=r+s

    content= requests.get(url).text
    ##读字段内容
    productModel=re.sub('":"',':',re.findall(r'"productModel":".*?"',content)[0].strip('"'))
    print(productModel)
    productTypeName=re.sub('":"',':',re.findall(r'"productTypeName":".*? ',content)[0].strip('"'))
    print(productTypeName)
    eName=re.sub('":"',':',re.findall(r'"eName":".*?"',content)[0].strip('"'))  ##名称
    print(eName)
    energyGrade=re.sub('":',':',re.findall(r'"energyGrade":.*?,',content)[0].rstrip(',').strip('"')) ##能效等级
    print(energyGrade)
    recordNum=re.sub('":"',':',re.findall(r'"recordNum":".*?"',content)[0].strip('"'))  ##备案号
    print(recordNum)
    recordDate=re.sub('":"',':',re.findall(r'"recordDate":".*?"',content)[0].strip('"')) ##公告时间

    ##存储
    file = open('data.txt', 'a')
    datelist=productModel,productTypeName,eName,recordNum,recordNum,recordDate
    writer = csv.writer(file)
    writer.writerow(datelist)


if __name__ == '__main__':
    inforead = codecs.open("urllist.txt", 'r', 'utf-8')
    starturl=inforead.readline()
    while starturl!="":
        starturl = starturl.rstrip('\r\n')
        get_infor(starturl)
        starturl = inforead.readline()
