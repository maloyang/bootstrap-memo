# app.py
# 1. session set / get
# 2. session clear
# 3. easy version login demo
# 4. you will be log out after 30 sec. by default

from flask import Flask, render_template, abort
from flask import make_response, request, jsonify, session, redirect, url_for
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def index():
    return '<h1>Hi index~</h1>'

@app.route('/sset')
def sset():
    '''
    session set test
    session加一個(key/value)pair --> (apple / iphone5)
    flask在return時就會把這東西丟出去
    client(Browser)那邊都會得到一個叫session的cookie(flask的預設名稱) --> 也就是session是存在cookie中的，但有編碼過
    因為是cookie所以每一次client移到每一個頁面都會把它送出來，
    因此Server可以得知這一個使用者的session值 --> 算是把session資料放在client端的cookie中
    '''
    session['apple'] = 'iphone5'
    return '<h1>session set</ht>'


@app.route('/sget')
def sget():
    return session.get('apple')

# set more session (key/value) pair
@app.route('/sset2')
def sset2():
    session['apple2'] = 'iphone6'
    session['apple3'] = 'iphone7'
    return '<h1>session set 2</h1>'

@app.route('/sget2')
def sget2():
    data = dict()
    data['username'] = session.get('username')
    data['apple'] = session.get('apple')
    data['apple2'] = session.get('apple2')
    return jsonify(data)


@app.route('/sget-all')
def sget_all():
    data = dict()
    for key in session:
        data[key] = session.get(key)
    return jsonify(data)


def print_session():
    data = dict()
    for key in session:
        data[key] = session.get(key)
    print('session: ', data)

@app.route('/session-clear')
def session_clear():
    if session:
        session.clear()
    return 'session clear!'

#---------------------
# 開始實作login功能

def db_get_user(username):
    # you must get user_list from DB in real case
    user_list = [
        {'username':'admin', 'password':'aaaa', 'location':'松山'},
        {'username':'malo', 'password':'bbbb', 'location':'左營'},
        {'username':'mimi', 'password':'cccc', 'location':'沙鹿'},
    ]
    for user in user_list:
        if user['username']==username:
            return user
    return None

    
def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    user_data = db_get_user(username)
    return user_data and user_data['password']==password

def is_session_timeout(time_login, max_time=60):
    print(time.time()-time_login)
    return (time.time()-time_login) > max_time


def requires_session_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print_session()

        s_username = session.get('username')
        s_password = session.get('password')
        s_time_login = session.get('time_login')
        print(s_username, s_password, '-->', check_auth(s_username, s_password))
        if (not check_auth(s_username, s_password)) or is_session_timeout(s_time_login):
            return redirect(url_for('login2'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login2', methods = ['GET', 'POST'])
def login2():
    print_session()

    if request.method == 'POST':
        session_clear()
        username = request.form['username']
        password = request.form['password']
        print('input: ', username, password)
        if check_auth(username, password):
            print("check_auth ok: ", username, password)
            session['username'] = username
            session['password'] = password
            session['time_login'] = time.time()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login2'))

    return '''
        <form action="" method="post">
            username: <input type="text" name=username><br>
            password: <input type="password" name="password"><br>
            <input type="submit" value="submit"><br>
        </form>
    '''

@app.route("/page1")
@requires_session_auth
def page1():
    s_username = session.get('username')
    return '<h1>here is page1</h1> (hi~ '+s_username+')' 

@app.route("/page2")
@requires_session_auth
def page2():
    s_username = session.get('username')
    return '<h1>here is page2</h1> (hi~ '+s_username+')' 


if __name__ == "__main__":
    app.run(debug=True)
