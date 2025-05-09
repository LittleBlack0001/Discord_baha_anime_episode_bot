# Discord動畫瘋(新番)爬蟲機器人
### 一個簡易的DC動畫瘋爬蟲機器人 簡易又容易上手~~
以最淺顯易懂的方式 讓大家大致理解爬蟲在做甚麼 順便讓動漫迷靠這支機器人來不錯過新番資訊?
## 適合
python新手 對程式有稍微認知的朋朋 動漫迷(?
## 須知
本機器人僅用於學術用途 並無任何營利行為
本機器人所參考的Github:https://github.com/teddy8997/Baha-animation-notify  
## 教學片(更新中 無法觀看)
https://www.youtube.com/watch?v=jUUZ737BGhU

---
爬蟲網站: [巴哈姆特動畫瘋](https://ani.gamer.com.tw/)
## 使用步驟(簡):                                    
  1.下載並且解壓縮檔案然後開啟setting.json

  2.輸入你的channel id跟token(99%完成)

  3.執行main.py程式碼
  
  補.使用前請先檢查是否所有模組是否都有下載到 大致上有:discord pandas bs4 BeautifulSoup json urllib requests 總之 如果有看到import旁有出現黃底曲線 八九成就是沒安裝到模組 
  範例:
  ```
  pip install discord
  ```
## 使用步驟(詳):  
  1.前往Discord applications創立一隻機器人(https://discord.com/developers/applications)

  2.下載此機器人的程式碼 解壓縮後使用編譯器開啟 ☆這邊強力推薦大家把檔案放在根目錄 這樣比較不會有中文路徑問題

  3.檢查程式碼是否有問題 若import後面有黃底曲線 則可能是沒安裝到模組 所以請使用以下指令來安裝模組 ☆安裝前 請先檢查電腦是否已設置python環境
  ```
  pip install (模組名)
  ```
  4.若程式碼都無誤 可至setting.json把TOKEN跟channel_id貼上去 ☆如何找到channel_id 請至想要動畫瘋傳送資訊的頻道點擊右鍵 應該就可看到了

  5.執行程式碼 可按照機器人的提示進行操作 : !help

  p.s.機器人指令前綴 傳送頻道訊息都可隨意更改 若想改不知怎麼改 可以先看註解 若還是看不懂 下方有我的聯絡方式 歡迎訊問我~~ ><
## 最新內容
# Version1.1(最新)
  1. 在舊版本中 爬蟲到新番時會直接傳送到Discord頻道上 因此導致了當過長時間沒運行(突然有一天想運行) 
     造成大量新番一次傳送到頻道 在此版本中修改成只接收特定新番內容 也就是說 它只接收使用者指定的新番名
     當該動漫更新時 只發送該番的資訊 
  2. 在本次版本中 也新增幾項指令讓此機器人更實用 如add指令(新增使用者想看的動漫) delete(刪除使用者原指定的動漫) delete_all(一次刪除使用者所有指定的動漫) 
     想看所有指令可用!help來查看
  3. 這邊來說明一下新版本機器人的運作方式 首先機器人會先爬蟲動畫瘋網站 把資訊存到grab.csv裡面 使用者可使用!add (動漫名)指令來追蹤想看的動漫新資訊 當!add的動漫更新時
     則把該番資訊傳送到Discord頻道上面 (!!!這邊要注意的是 !add動漫必須更動畫瘋一樣 不然不會起作用 其他如delete指令也是 名字都必須一樣) 新增動漫數無限制 但請留意名字需相同
  p.s.剩餘的等之後教學片發布 這樣大家比較好理解!!!>< 有問題都可以滑到下方的聯絡方式詢問== 

## 簡易運作流程:
# Version1.1(最新)
   <ul>                                        
        <li>1.爬取動畫瘋資訊</li>
        <li>2.把讀取到的title跟episode跟原本裡面的.csv檔案做比對</li>
        <li>3.如果比對內容有新內容 則把新的資訊放入grab.csv檔案</li>
        <li>4.比對user_input_records.csv如果有與grab.csv相同名稱 且grav.csv有更新新內容 </li>
        <li>5.把新資訊傳送到Discord頻道上面</li>
        <li>5.重複執行</li>
      </ul>
# Version1.0
   <ul>                                        
        <li>1.爬取動畫瘋資訊</li>
        <li>2.把讀取到的title跟episode跟原本裡面的.csv檔案做比對</li>
        <li>3.如果比對內容有新內容 則把新的資訊放入.csv檔案</li>
        <li>4.把新的資訊傳送到Discord</li>
        <li>5.重複執行</li>
      </ul>

## 補充
<ul>
  <li>I:如果想讓機器人能即時收到新番資訊 建議永久開著</li>
  <li>II:程式碼註解由我親手撰寫 如果有錯誤請見諒</li>
</ul>

## Q&A常見問題
<h4>1.Q:為甚麼import右邊會出現黃底曲線?</h4>
<h5>A:八九成是沒安裝到模組 請看之前所說的方式安裝 再不懂可上網查詢或私訊我owo</h5>

<h4>2.Q為何一開始運作的時候 會大量跑出動漫資訊 是不是程式碼出問題?</h4>  
<h5>A:此問題是正常的 由於CSV檔存的是我之前存上去的爬蟲 所以剛開始出現大量新番資訊是正常的 大概2-3次讀取 就會正常了!!! (程式碼執行後新資訊會開始大量覆寫之前存的CSV檔 故剛開始運作出現大量新番資訊 不是程式碼有問題)</h5>

<h4>3.Q:之後還會更新機器人嗎?</h4>
<h5>A:會的 只要我有時間 就一定會更新機器人 新增一些功能?</h5>

<h4>4.Q:為甚麼在終端機會看到print等輸出? 程式碼例:print("test") 終端機:test</h4>
<h5>A:之前程式碼運作常遇到問題 所以分段測試輸出 只是忘記刪掉 請忽視它@@ 看不順眼 可刪掉owo</h5>

## 聯絡方式
<ul>
  <li>Discord:xiaoheio1106</li>
  <li>Gmail:grass102120@gmail.com</li>
</ul>
多問我問題 好讓我多打Q&A??? 哀斗...程式碼註解打到睡著 所以裡面可能有點亂QQ 懶得改哈哈

## 爬蟲結果展示
![Screenshot 2024-01-02 202521](https://github.com/LittleBlack0001/Discord_baha_new_episode_bot/assets/87685533/365df7bc-0d14-445f-b56a-9308d2649648)


