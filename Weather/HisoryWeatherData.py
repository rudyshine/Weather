# encoding=utf-8
import codecs
import requests
import json
import pymongo
import time
import pandas as pd

def request(year, month,idNumber):
    url = "http://d1.weather.com.cn/calendar_new/"+year+"/"+str(idNumber)+"_"+year+month+".html?_=1513081038706"
    # urllist = pd.DataFrame({'url':url})
    # table = urllist.set_index('data_text')
    # table.head()
    # urllist.to_csv(' weibo_data.csv', mode='a')
    # print("done save csv....")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Referer": "http://www.weather.com.cn/weather40d/101280701.shtml",
    }
    return requests.get(url, headers=headers)

def parse(res):
    time.sleep(3)
    json_str = res.content.decode(encoding='utf-8')[11:] #获取数据
    return json.loads(json_str)

def save(list):
    subkey = {'date': '日期','hmax': '最高温度', 'hmin': '最低温度', 'hgl': '湿度', 'fe': '节日', 'wk': '星期', 'time': '发布时间'}
    idNumbers={'城市ID': idNumber}
    for dict in list:
        subdict = {value: dict[key] for key, value in subkey.items()}   #提取原字典中部分键值对，并替换key为中文
        subdict.update(idNumbers)  #加入城市ID
        forecast.insert_one(subdict)      #插入mongodb数据库


def getInfo():
    year = "2016"
    month = 1
    for i in range(month, 13):
        month = str(i) if i > 9 else "0" + str(i)  # 小于10的月份要补0
        save(parse(request(year, month,idNumber)))
        time.sleep(3)



if __name__ == '__main__':

    client = pymongo.MongoClient('172.28.171.13', 27017)   # 连接mongodb,端口27017
    test = client['WeatherData']                              # 创建数据库文件test
    forecast = test['HistoryData2016']                        # 创建表forecast
    inforead = codecs.open("urllist_ID.txt", 'r', 'utf-8')
    idNumber = inforead.readline()
    while idNumber != "":
        idNumber = idNumber.rstrip('\r\n')
        try:
            getInfo()
        except :
            print('IP被封1，程序休息当前ID为：' + idNumber)
            time.sleep(600)
            try:
                getInfo()
            except :
                print('IP被封2，程序休息当前ID为：' + idNumber)
                time.sleep(3600)
                try:
                    getInfo()
                except :
                    print("IP被封"+ idNumber)
        idNumber = inforead.readline()
        print(idNumber)
