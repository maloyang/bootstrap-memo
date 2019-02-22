# basic-auth範例，多帳號，每個帳號有不同的設定

- 用basic auth登入
- 使用者帳戶放在DB中(先放在mongoDB中的demo2-3-user中)
- 每一個帳戶資料要記錄所在地點，作為登入頁面要載入哪一個地點資料的依據
```
{
    'username':'admin',
    'password':'123456',
    'location':'古亭',
}
```
- 這邊利用的技巧是因為basic auth會在每一次要送request時，把帳號送出一次，我們就可以知道目前Browser登入的人是誰
- 如 `/aqi-history-get` 因為有加 `@requires_auth` 所以Browser會送帳密過來，我們就可以用username去查這個帳號的權限(在這邊是「地點」)

## basic auth 好像沒有登出的機制，所以要切不同帳號測試，就…

## 接著應該來試試session的登入機制!! 做有登出，登入的功能應該會比較好

