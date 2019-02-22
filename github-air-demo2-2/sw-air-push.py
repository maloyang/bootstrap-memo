# -*- coding: utf-8 -*-

# 2019-01-11
#   1. 收集env. air資訊寫入mongoDB中

import requests
import time

import os
import datetime
from pymongo import MongoClient
import urllib.request
#from six.moves import urllib #use this in python2
import json


def cron_job_AQI_push_DB():
    str_time = time.strftime("%Y%m%d %H%M%S", time.localtime())
    print('[%s] push AQI to mongoDB' %(str_time) )
    url = 'http://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
    urllib.request.urlretrieve(url, "AQI.json")
    f = open("AQI.json", 'rb')
    jdata = f.read().decode('utf8')
    f.close()
    data = json.loads(jdata)
    
    # 整理資料，因為mongoDB的key不能有 "_" 以外的特殊符號，但AQI中有 PM2.5 , PM2.5_AVG這樣的數據
    for site_data in data:
        if 'PM2.5' in site_data:
            site_data['PM2p5'] = site_data.pop('PM2.5')
        if 'PM2.5_AVG' in site_data:
            site_data['PM2p5_AVG'] = site_data.pop('PM2.5_AVG')

    db_insert_many(data, 'AQI')
    db_insert_many_rt(data, 'AQI_rt')

def db_insert_many(my_data, coll_name='my_coll'):
    db_url = 'mongodb://heroku_r1v4g1s0:e2nfsp20klh8svep0fh2vhb2c3@ds147125.mlab.com:47125/heroku_r1v4g1s0'
    #db_url = os.environ['MONGODB_URI']
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # insert
    res = my_coll.insert(my_data)
    return len(res)

def db_insert_many_rt(my_data, coll_name='my_coll'):
    """
    rt: only one data every uid
    """
    db_url = 'mongodb://heroku_r1v4g1s0:e2nfsp20klh8svep0fh2vhb2c3@ds147125.mlab.com:47125/heroku_r1v4g1s0'
    #db_url = os.environ['MONGODB_URI']
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # insert
    my_coll.remove() # remove all item of uid
    res = my_coll.insert(my_data)
    return len(res)



if __name__ == "__main__":
    str_time = time.strftime("%Y%m%d %H%M%S", time.localtime())
    now = datetime.datetime.now()
    if now.minute==20:
        cron_job_AQI_push_DB()
