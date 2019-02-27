# 使用Session完成登入功能，多帳號，每個帳號有不同的設定

- 用session實作登入
- 每一個帳戶資料要記錄所在地點，作為登入頁面要載入哪一個地點資料的依據
- 加入Logout功能

----

## 參考資料如下

### Flask cookie & session
- 參考了這一篇還不錯! [flask基礎七之狀態保持cookie和session](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/396239/)
    - session 看起來是存在名為session的cookie中 (browser side)
    - cookie最大可存4kb --> 所以session也只能這麼大
    - 每次session傳給browser後，因為是cookie，所以每一次browser都會回傳，因此可以知道上一次的資料
    - 這邊有個只太了解的地方，這個名為session的cookie的期限不知道是多少，只看他寫了一個session....


### 如何設定session，並傳出去
- 先import session
    - `from flask import session`


- 設定session中的key/value，送出時，自動會帶出去
```
@app.route('/sset')
def sset():
    session['username'] = 'itcast'
    return '<h1>session set</ht>'
```


- 用這樣取session資料
```
@app.route('/sget')
def sget():
    return session.get('username')
```


- 也可以一次設定多個變數
```
@app.route('/sset2')
def sset2():
    session['apple'] = 'iphone'
    session['apple2'] = 'iphone2'
    return '<h1>session set</ht>'
```


- 一次要把session中的資料讀回來用這樣，session不是dict，所以不能直接用jsonify包起來
```
@app.route('/sget4')
def sget4():
    data = dict()
    for key in session:
        data[key] = session.get(key)
    return jsonify(data)
```
