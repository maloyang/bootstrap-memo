# bootstrap-memo
some memo. for bootstrap

## 觀看教學1 <bootstrap4 教學01> [link](https://www.youtube.com/watch?v=xwFLdiFfXmI)

- http://getbootstrap.com/
- 點expo --> 看一些採用bootstrap且設計的不錯的網頁
- 特色:
  - grid
  - responsive, 響應式設計, 進到網頁時可以依user的裝置自適應為較佳的版面
- bootstrap3 or 4?
  - bootstrap4: 有較新的功能，但是ie9,10才能支援(ie9也不是很好)
  - 如果要讓ie8能使用，建議使用bootstrap3
  
## 觀看教學2 <bootstrap4  教學02> [link](https://www.youtube.com/watch?v=kax6QO6GP88)
- 進到這一頁：http://getbootstrap.com/docs/4.1/getting-started/introduction/
- 先把bootstrap4的css引入，其中integrity後面接的一串文字是為了讓browser確認css檔是否正確(像md5的東西吧)，避免.css檔被修改植入不該有的東西。
  `<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">`
- 而其中「crossorigin="anonymous"」這一段是安全性的措施，因為我們的css跨網域存取，因此存取時可能被要求cookie, session的資訊，用anonymous是比較安全的方式
- 當然不加入integrity, crossorigin這二個項目網頁也是會正常的，只看你認為有沒有必要。

  
