# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import random
import time
import requests
import urllib.request
#import json
import ssl
import datetime

from flask import Flask, request, abort, render_template
from flask import json, jsonify
from flask_cors import CORS, cross_origin # for cross domain problem

from pymongo import MongoClient


#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

mongo_url = os.getenv('MONGODB_URI', None)


@app.route('/ok')
def homepage():
    the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())    
    return 'ok. time is ' + the_time

@app.route('/')
@app.route('/airbox')
def airbox():
    #return render_template('index.html')
    return app.send_static_file('index.html')

@app.route('/login.html')
def login():
    #return render_template('login.html')
    return app.send_static_file('login.html')



@app.route('/aqi-rt-get', methods=['GET', 'POST'])
def aqi_rt_get():
    aqi_rt = db_rt_get('AQI_rt')
    print('aqi_rt:', aqi_rt)
    return jsonify(aqi_rt)

@app.route('/aqi-history-get_my', methods=['GET', 'POST'])
def aqi_history_get_my():
    aqi_data = db_aqi_history_get()
    print('aqi_rt:', aqi_data)
    return jsonify(aqi_data)

def db_aqi_history_get(coll_name='AQI', mySiteName='鳳山', tm_start=None, tm_end=None):
    #db_url = 'mongodb://heroku_bpw5rldp:2qj7dvv1np8buehthlp1f4l41v@ds127771.mlab.com:27771/heroku_bpw5rldp'
    db_url = os.environ['MONGODB_URI']
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # check time and find data
    if tm_start:
        if tm_end:
            res = my_coll.find({'SiteName':mySiteName, 'PublishTime':{'$gte':tm_start, '$lte':tm_end}}, {'_id':0})
        else:
            res = my_coll.find({'SiteName':mySiteName, 'PublishTime':{'$gte':tm_start}}, {'_id':0})
    else:
        my_time = datetime.datetime.now()
        day_offset = datetime.timedelta(hours=8)
        my_time = my_time + day_offset
        str_time = my_time.strftime("%Y-%m-%d")        
        res = my_coll.find({'SiteName':mySiteName, 'PublishTime':{'$gte':str_time+' 00:00', '$lte':str_time+' 23:59'}}, {'_id':0})
    return list(res)

def db_rt_get(coll_name='my_coll'):
    db_url = os.environ['MONGODB_URI']
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # find
    res = my_coll.find({}, {'_id':0})
    return list(res)


def db_insert_many(my_data, coll_name='my_coll'):
    db_url = os.environ['MONGODB_URI']
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
    db_url = os.environ['MONGODB_URI']
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # insert
    my_coll.remove() # remove all item of uid
    res = my_coll.insert(my_data)
    return len(res)


############
# 從opendata爬資料的測試
############
@app.route('/aqi', methods=['GET', 'POST'])
def aqi_push_DB():
    str_time = time.strftime("%Y%m%d %H%M%S", time.localtime())
    print('[%s] /aqi push AQI to mongoDB' %(str_time) )
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
    #print('AQI-data:\r\n', data)
    return jdata


if __name__ == "__main__":
    app.run()
