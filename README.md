# Discord動畫瘋(新番)爬蟲機器人
### 一個簡易的DC爬動畫瘋der機器人 簡易又容易上手~~
以最前顯易懂的方式 讓大家大致理解爬蟲在做甚麼 順便讓動漫迷靠這支機器人來不錯過新番資訊?
## 須知
本機器人僅用於學術用途 並無任何營利行為
本機器人所參考的Github:https://github.com/teddy8997/Baha-animation-notify  

---
爬蟲網站: [巴哈姆特動畫瘋](https://ani.gamer.com.tw/)
## 使用步驟:                                    
  1.下載並且解壓縮檔案然後開啟setting.json

  2.輸入你的channel id跟token(99%完成)
  
  補.使用前請先檢查是否所有模組是否都有下載到 大致上有:discord pandas bs4 BeautifulSoup json urllib requests 總之 如果有看到import旁有出現黃底曲線 八九成就是沒安裝到模組 
  範例:
  ```
  pip install discord
  ``` 

## 運作流程:
   <ul>                                        
        <li>1.爬取動畫瘋資訊</li>
        <li>2.把讀取到的title跟episode跟原本裡面的.csv檔案做比對</li>
        <li>3.如果比對內容有新內容 則把新的資訊放入.csv檔案</li>
        <li>4.把新的資訊傳送到Discord</li>
        <li>5.重複執行</li>
      </ul>

## 補充
I:如果想讓機器人能及時收到新番資訊 建議永久開著
II:程式碼註解由我親手撰寫 如果有錯誤請見諒

## Q&A常見問題
<h5>1.Q:為甚麼import右邊會出現黃底曲線?</h5>
<h5>A:八九成是沒安裝到模組 請看之前所說的方式安裝 再不懂可上網查詢或私訊我owo</h5>

<h5>2.Q為何一開始運作的時候 會大兩跑出動漫資訊 是不是程式碼出問題?</h5>  
<h5>A:此問題是正常的 由於CSV檔存的是我之前存上去的爬蟲 所以剛開始出現大量新番資訊是正常的 大概2-3次讀取 就會正常了!!! (程式碼執行後新資訊會開始大量覆寫之前存的CSV檔 故剛開始運作出現大量新番資訊 不是程式碼有問題)</h5>

<h5>3.Q:之後還會更新機器人嗎?</h5>
<h5>A:會的 只要我有時間 就一定會更新機器人 新增一些功能?</h5>

<h5>4.Q:為甚麼在終端機會看到print等輸出? 程式碼例:print("test") 終端機:test</h5>
<h5>A:之前程式碼運作常遇到問題 所以分段測試輸出 只是忘記刪掉 請忽視它@@ 看不順眼 可刪掉owo</h5>

## 聯絡方式
<ul>
  <li>Discord:xiaoheio1106</li>
  <li>Gmail:grass102120@gmail.com</li>
</ul>
多問我問題 好讓我多打Q&A??? 哀斗...程式碼註解打到睡著 所以裡面可能有點亂QQ 懶得改哈哈

## 爬蟲結果展示
![Screenshot 2024-01-02 202521](https://github.com/LittleBlack0001/Discord_baha_new_episode_bot/assets/87685533/365df7bc-0d14-445f-b56a-9308d2649648)


