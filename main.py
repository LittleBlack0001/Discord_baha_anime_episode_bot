import discord
from discord.ext import commands, tasks
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import json
import urllib.request

def tiep(title, episode, oldcsv): #讀取是否為新的title episode
    result = False
    for idx, row in oldcsv.iterrows():  #看oldcsv每一列
        if title == row['title'] and episode == row['episode']:
            result = True
    return result

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html                                             #發送請求
def output_organized(s):
    output=''
    output += '>>> ## 名稱: __**' + s['title'] + '**__\n'
    output += "### 集數: " +s['episode'] + '\n'
    output += "### 發布日期:2023/"  + str(s['date']) +'        '+"發布時間: "+ str(s['time']) + '\n'  #因年份無法爬取 故直接在這邊打 所以到達隔年的話 年份也必須手動從這邊修改
    output += "### 網址: " +s['url'] + '\n'                      #62-64會將爬蟲的資訊放到discord指定channel上面 註解:此處格式已都整理好 圖片在github上面 要修改請自行修改

    return output

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!',intents = intents)             #discord bot的基本格式 

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    channel = bot.get_channel(int(jdata['channel_id']))   # TRY  channel = client.get_channel(COPY DISCORD CHANNEL ID)
    if channel is not None:
        await channel.send('更新中......')
        send_product_df.start()
    else:
        print('找不到指定的頻道！')                         #此處是判斷執行中機器人是否已經到達指定的channel上面 有的話會跑出更新中...(在頻道上面) 若沒有的話會直接到(終端機)發送找不到頻道

@tasks.loop(minutes=1)   #迴圈設定 每分鐘爬蟲動畫瘋網站 每分鐘設定是為了一些能24hr開的人設計 盡量能準時爬取到新番資訊
async def send_product_df():
    print("test")   #測試1 if有讀到 則印出print
    url = "https://ani.gamer.com.tw/"   #爬蟲巴哈姆特動畫瘋網站
    req_bs = bs(get_html(url), "html.parser")
    contents_wrapper = req_bs.find(class_="newanime-wrap timeline-ver")
    if contents_wrapper is None:
        print("contents_wrapper is None")
        return
    contents = contents_wrapper.findAll(class_=re.compile(r"anime-content-block"))
    dateinfo = contents_wrapper.findAll(class_=re.compile(r"anime-date-info anime-date-info-block-arrow"))
    output = []
    b = pd.read_csv("grab.csv", encoding='utf-8')   #utf-8 建立csv檔案並把爬蟲到的資料爬到.csv檔案裡
    for i in range(len(contents)-5):
        title = contents[i].find(class_="anime-name_for-marquee").text
        url = contents[i].find(class_="anime-card-block").get("href")
        date = ''.join(i for i in dateinfo[i].text if i.isdigit() or i=='/')
        time = contents[i].find(class_="anime-hours-block").find(class_="anime-hours").text    
        try:
            episode = contents[i].find(class_="anime-episode").find('p').text
        except AttributeError:
            episode = contents[i].find(class_="label-edition color-OVA").text     #抓其中較好判斷的兩個 然後進行簡易爬取資訊 若資料有與讀取到的兩個相同則覆寫(ex.EVA 第一集 -> 覆寫 -> EVA 第二集)
        finally:
            if tiep(title, episode, b) == False:  #如果tiep讀取到新的thing == False(上面)加入71行
                output.append({
                    "title": title,
                    "url": url,
                    "episode": episode,
                    "date": date,
                    "time": time
                })
    df = pd.DataFrame(output)
    if len(df) != 0:
        df['url'] = "https://ani.gamer.com.tw/" + df['url'].astype(str)
    channel = bot.get_channel(int(jdata['channel_id']))   #抓取頻道 並把爬蟲到的新資料(尚未或剛載到CSV檔案的爬蟲資訊印到頻道上面)  註解:此處是把網站及集數的sn=?????整理好 然後發到discord頻道上面
    print("end")    #測試2
    print(len(df.to_string()))
    print(df.to_string())
    for idx, row in df.iterrows(): #df現在是新的
        b.loc[len(b)] = {'title':row['title'], 'episode':row['episode']}  #用row把新列表丟到舊列表裡面
        await channel.send(output_organized(df.loc[idx,:]))  #0:2列,行  ":"讀取所有那欄東西(取全部)
    b = b.tail(100)  #csv最多占存100(1-101)筆(爬蟲資料
    b.to_csv('grab.csv',index=False, encoding='utf-8')  #新的都處理好後 在更新舊的csv
    
bot.run(jdata['TOKEN'])
