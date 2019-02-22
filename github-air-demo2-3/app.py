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

from functools import wraps
from flask import Flask, request, abort, render_template, Response
from flask import json, jsonify
from flask_cors import CORS, cross_origin # for cross domain problem

from pymongo import MongoClient


#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

#mongo_url = os.getenv('MONGODB_URI', None)
mongo_url = 'mongodb://heroku_r1v4g1s0:e2nfsp20klh8svep0fh2vhb2c3@ds147125.mlab.com:47125/heroku_r1v4g1s0'


def db_get_user(username):
    # you must get user_list from DB in real case
    user_list = [
        {'username':'admin', 'password':'aaaa', 'location':'松山'},
        {'username':'malo', 'password':'2222', 'location':'左營'},
        {'username':'mimi', 'password':'cccc', 'location':'沙鹿'},
    ]
    for user in user_list:
        if user['username']==username:
            return user
    return None
    
    
#== for basic auth.
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    #return username == 'admin' and password == '12345'
    user_data = db_get_user(username)
    return user_data and user_data['password']==password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify. You have to login.', 
    401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#==--

@app.route('/ok')
def homepage():
    the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())    
    return 'ok. time is ' + the_time

@app.route('/')
@app.route('/airbox')
@requires_auth
def airbox():
    auth = request.authorization #-->如果有多個user，可以從這邊取得username
    print(auth) #--> {'username': 'admin', 'password': '12345'}
    #return render_template('index.html')
    return app.send_static_file('index.html')
 
@app.route('/aqi-rt-get', methods=['GET', 'POST'])
def aqi_rt_get():
    aqi_rt = db_rt_get('AQI_rt')
    # change to local json file for demo
    #aqi_rt = load_json_file('aqi-rt-get.json')

    #print('aqi_rt:', aqi_rt)
    return jsonify(aqi_rt)

@app.route('/aqi-history-get_my', methods=['GET', 'POST'])
def aqi_history_get_my():
    aqi_data = db_aqi_history_get()
    # change to local json file for demo
    #aqi_data = load_json_file('aqi-history-get_my.json')

    #print('aqi_history:', aqi_data)
    return jsonify(aqi_data)

@app.route('/aqi-history-get', methods=['GET', 'POST'])
@requires_auth
def aqi_history_get():
    #由auth的帳號決定回傳哪個地點的資訊
    auth = request.authorization #-->如果有多個user，可以從這邊取得username
    if auth:
        user_data = db_get_user(auth.username)
        print(user_data)
        aqi_data = db_aqi_history_get(coll_name='AQI', mySiteName=user_data['location'])
        # change to local json file for demo
        #aqi_data = load_json_file('aqi-history-get_my.json')

        #print('aqi_history:', aqi_data)
        return jsonify(aqi_data)

def load_json_file(filename):
    data = None
    with open(filename) as f:
        data = json.load(f)
    return data

def db_aqi_history_get(coll_name='AQI', mySiteName='鳳山', tm_start=None, tm_end=None):
    db_url = mongo_url
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
        day_offset = datetime.timedelta(hours=0)
        my_time = my_time + day_offset
        str_time = my_time.strftime("%Y-%m-%d") 
        print(str_time)       
        res = my_coll.find({'SiteName':mySiteName, 'PublishTime':{'$gte':str_time+' 00:00', '$lte':str_time+' 23:59'}}, {'_id':0})
    return list(res)

def db_rt_get(coll_name='my_coll'):
    db_url = mongo_url
    client = MongoClient(db_url)
    db = client[db_url.split('/')[-1]]
    my_coll = db[coll_name] #get collection
    # find
    res = my_coll.find({}, {'_id':0})
    return list(res)


def db_insert_many(my_data, coll_name='my_coll'):
    db_url = mongo_url
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
    db_url = mongo_url
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
    app.run(debug=True)
