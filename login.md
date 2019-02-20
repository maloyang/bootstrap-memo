# 使用Flask實做網頁登入

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
