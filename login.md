# 使用Flask實做網頁登入

## basic auth.
這是一個比較簡單的實現方式，一般在嵌入式系統的網頁設定頁面常會使用這樣的認證方式來登入

- [參考說明](https://zh.wikipedia.org/wiki/HTTP%E5%9F%BA%E6%9C%AC%E8%AE%A4%E8%AF%81)
- 當沒有通過這一個認證時，會回傳一個「HTTP 401 錯誤 - 未授權 (Unauthorized)」的錯誤
- 使用時要了解[decorator](https://realpython.com/primer-on-python-decorators/#simple-decorators)
- [參考文章2](https://medium.com/origino/user-authentication-2d7d8d08e108)

### 剛在Flask的extension突然發現了[Flask-Basic-Auth](https://flask-basicauth.readthedocs.io/en/latest/)
這個讓你使用Basic-Auth可以少寫很多code啊!! 真棒



## session
- [參考文章1](http://fred-zone.blogspot.com/2014/01/web-session.html)
  - Server/Client 是沒有常態連線的，因此Server不會知道Client的狀態是否有登入
  - session不一定要cookie
  - session: 訂餐後取得的號碼牌
  - 最原始的session: 多把資料存在Server中，即你點了什麼都放在Server中(RAM, DB, ...)，要拿號碼牌來查你的餐點
    - 我要的就是小系統，所以這是我想實作的方式
  - session的實現法：(1)cookie -> 現在的網站框架中，預設多採用cookie ; (2)直接把session輸出到網頁中
  - 所以 cookie-base-session被視為一解決方案：把資料暫存在cookie，讓client自己保存 --> 即把你的餐點全寫在號碼牌上
  - cookie有被竄改的風險，所以一般會加密，只有server才知道怎麼解 (當然，也有可能被破)


