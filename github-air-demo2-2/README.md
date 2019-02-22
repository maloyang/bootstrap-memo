# 使用 basic-auth，但需要出個帳號時

## 我們假設user_list是由DB取出來的
```
def db_get_user_list():
    user_list = {
        'admin':    '123456',
        'mimi':     'cchaha',
        'malo':     '123321'
    }
    return user_list
```

## 在確認帳密的部份改如下，這樣就可以把本來寫死在code中的單一帳密改為多個帳密了
```
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    #return username == 'admin' and password == '12345'
    user_list = db_get_user_list()
    if username in user_list:
        return user_list[username]==password
    return False
```
