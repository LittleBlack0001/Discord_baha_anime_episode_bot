import discord
from discord.ext import commands, tasks
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import json
import urllib.request 
import asyncio  

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
    output += "### 發布日期:2024/"  + str(s['date']) +'        '+"發布時間: "+ str(s['time']) + '\n'  #因年份無法爬取 故直接在這邊打 所以到達隔年的話 年份也必須手動從這邊修改
    output += "### 網址: " +s['url'] + '\n'                      #將爬蟲的資訊放到discord指定channel上面 註解:此處格式已都整理好 圖片在github上面 要修改請自行修改
    return output

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!',intents = intents)             #discord bot的基本格式 command_prefix='' ''內為機器人前綴 可隨意調整

user_input_records = pd.DataFrame(columns=['title'])

bot.remove_command('help') #discord原本已存在help 所以必須先清除 以便之後新增方便

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    channel = bot.get_channel(int(jdata['channel_id']))   # TRY  channel = client.get_channel(COPY DISCORD CHANNEL ID)
    if channel is not None:
        await channel.send('### 機器人已啟動輸入: !help可察看所有指令')
        send_product_df.start(channel)
    else:
        print('找不到指定的頻道！')                         #此處是判斷執行中機器人是否已經到達指定的channel上面 有的話會跑出更新中...(在頻道上面) 若沒有的話會直接到(終端機)發送找不到頻道

@tasks.loop(minutes=1)   #迴圈設定 每分鐘爬蟲動畫瘋網站 每分鐘設定是為了一些能24hr開的人設計 盡量能準時爬取到新番資訊
async def send_product_df(channel):
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
    for i in range(len(contents) - 5):
        title = contents[i].find(class_="anime-name").text
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
    print("end")    #測試2
    print(len(df.to_string()))
    print(df.to_string())
    
    watchlist = pd.read_csv("user_input_records.csv", encoding='utf-8') #讀取user.csv的內容
    for idx, row in df.iterrows():
        b.loc[len(b)] = {'title': row['title'], 'episode': row['episode']}
        if row['title'] in list(watchlist['title']):    #判斷新增動畫在user.csv的title 在讀取grab.csv如果有新的則把新資訊發送到 discord channel #series轉成list 
            await channel.send(output_organized(df.loc[idx, :]))
    b = b.tail(10000)
    b.to_csv('grab.csv', index=False, encoding='utf-8')

#==============================================   new   ============================================================

@bot.command(help = "檢視所有指令")  
async def help(ctx):    #help指令 查看機器人所有指令 help = "" 當輸入help時會出現註解
    help_message = "# 以下是可用的命令列表：\n\n"
    for command in bot.commands:
        help_message += f"**!{command.name}**: {command.help}\n"   #get所有已知指令    如果在第26行更改前綴 請把 f"**!{command.name}裡的"!"改成您更改後的前綴 不然當輸入help時 會出現原本的前綴
    await ctx.send(help_message)


@bot.command(help = "新增動漫名(動漫名必須和動畫瘋一樣):/add (動漫名)")
async def add(ctx, *, anime_name):    #add指令 把使用者add的資料(title)儲存進user_input_records.csv裡面

    df = pd.read_csv("user_input_records.csv", encoding='utf-8')
    new_record = pd.DataFrame({'title': [anime_name]})
    user_input_records = pd.concat([df, new_record], ignore_index=True)
    user_input_records.to_csv("user_input_records.csv",index=False , encoding='utf-8')
    await ctx.send(f"已新增動漫: {anime_name}")


@bot.command(help = "刪除已儲存的動漫(必須跟原輸入相同):/delete (動漫名)")
async def delete(ctx, *, anime_name):   #delete指令 指定刪除使用者存入user_input_records.csv裡面的資料(title)
    channel = ctx.channel
    df = pd.read_csv("user_input_records.csv", encoding='utf-8')
    if anime_name not in df['title'].values:
        await ctx.send("無法找到指定動漫！")
        return
    df = df[df['title'] != anime_name]
    df.to_csv("user_input_records.csv", index=False, encoding='utf-8')
    await ctx.send(f"刪除成功！")

@bot.command(help = "刪除所有動漫")
async def delete_all(ctx):  #delete_all指令 一次性刪除使用者存入存入user_input_records.csv裡面的資料(title)
    channel = ctx.channel
    df = pd.read_csv("user_input_records.csv", encoding='utf-8')
    if df.empty:
        await ctx.send("目前無儲存任何動漫！")
        return
    else:
        confirmation_message = await ctx.send("您確定要刪除全部嗎？刪除將無法復原 請輸入(yes/no)")  #二次確認 防止手癢黨不小心按到 
        while True:  # 迴圈判斷
            try:
                confirmation = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)  #接收使用者輸入訊息 如果超過10sec則取消操作
                if confirmation.content.lower() == "yes":   #當使用者輸入yes則刪除全部動漫
                    df = pd.DataFrame(columns=['title'])  
                    df.to_csv("user_input_records.csv", index=False, encoding='utf-8')
                    await ctx.send("已刪除全部動漫！")
                    break 
                elif confirmation.content.lower() == "no": #當使用者輸入no時則取消操作
                    await ctx.send("取消操作！")
                    break 
                else:
                    await ctx.send("請輸入'yes'或'no'！")  #當使用者輸入yes/no以外內容時 繼續等待再次輸入直到輸入yes/no才break或者等到時間到則stop
            except asyncio.TimeoutError:
                await ctx.send("操作超時，取消操作！")
                break  
        
@bot.command(help="列出所有已儲存的動漫: !check") 
async def check(ctx):                    #check指令 查看使用者目前已存入的資料(title)
    channel = ctx.channel
    df = pd.read_csv("user_input_records.csv", encoding='utf-8')
    if df.empty:                            #檢查user_input_records.csv有無儲存內容
        await ctx.send("目前沒有儲存任何動漫！")
    else:
        await ctx.send("# 目前已儲存的動漫:")
        for idx, row in df.iterrows():
            await ctx.send(row['title'])   #把user_input_records.csv裡面的資料(title)都print到頻道上

bot.run(jdata['TOKEN'])



