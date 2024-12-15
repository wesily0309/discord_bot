import asyncio
from enum import Enum
import discord
import asyncio
from discord.ext import commands,tasks
import datetime
import json
import os

intents = discord.Intents.all()
intents.members = True
#client = discord.Client(intents=intents)
client= commands.Bot(command_prefix='!', intents=intents)

#bot = commands.Bot(command_prefix="!")
#slash = SlashCommand(bot, sync_commands=True)
cfg={}
with open(r'config.json',mode='r',encoding='utf-8') as t:
    cfg=json.load(t)
botid=cfg['botid']#讀檔接入
#role_names = ['位驗證', '以驗證']
role_names = [cfg['not_verify_role'], cfg['verify_role']]
print(cfg["h"],type(cfg["m"]))
############
# 臺灣時區 UTC+8
tz = datetime.timezone(datetime.timedelta(hours = 8))
    # 設定每日十二點執行一次函式
everyday_time = datetime.time(hour = cfg["h"], minute = cfg['m'], tzinfo = tz)
@tasks.loop(time = everyday_time)
async def everyday():
#    print("aaaa")
    trole=None
#    now=datetime.datetime.now()
    gid=client.get_guild(cfg["server_id"])
#    now=datetime.datetime.now()

    for r in gid.roles:
        if r.name==cfg['verify_role']:
            trole=r
            break
        else:
            print("找不到身分組")
    for member in trole.members:
        await member.remove_roles(trole)
        print(f"已清除{member.name}的權限")


#########
@client.event
async def on_ready():
  everyday.start()
  print(f"目前登入身份 --> {client.user}")
  game = discord.Game("Type @AliceBot help or a!help")
  await client.change_presence(status=discord.Status.online, activity=game)
  print('機器人目前已在線上')

@client.event
async def on_presence_update(before, after):
    if before.status != after.status:
        print(f'{before.name} is now {after.status} in {after.guild.name}|time:{datetime.datetime.now()}')
        with open(r"log.txt", mode="a",encoding='utf-8') as f:
            f.write(f'{before.name} is now {after.status} in {after.guild.name}|time:{datetime.datetime.now()} + \n')
'''
            user = message.author
            guild = message.guild
            required_role = discord.utils.get(guild.roles, name=role_names[0])

            if required_role in user.roles:
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    with open(r'message_log.txt',mode='a',encoding='utf-8') as ll:
        ll.write(f'{datetime.datetime.now()}|{message.guild.name}{message.channel.name}{message.author}message:{message.content}\n')
    print(f'{datetime.datetime.now()}|{message.guild.name}{message.channel.name}{message.author}:{message.content}\n')
    role = discord.utils.get(message.guild.roles, name=role_names[0])#
    role_v = discord.utils.get(message.guild.roles, name=role_names[1])
    #print(role_v,role)
    if role in message.author.roles:
        if message.content.startswith("<@{botid}> ontop"):  #ontop!!!
                letters = message.content[28:]
                result = letters + " on top!!!"
                await message.channel.send(result)

        elif message.content == "a!help":  #help-reply
                ahelp = discord.Embed(
                    title="指令的各種使用方法",
                    description=
                    """ a!help顯示指令功能 \n
                    a!unverify 解除權限 \n
                    a!verify <密碼>#開啟管理員權限 \n
                    a!copy <數量>#備份當前頻道訊息\n
                    a!clear <數量>備份當前頻道訊息 \n
                    a!say<訊息>發送匿名訊息"""
                )
                await message.channel.send(embed=ahelp)

        elif message.content == "<@{botid}> help":  #help-reply
                ahelp = discord.Embed(
                    title="指令的各種使用方法",
                    description=
                    " a!help顯示指令功能 \n a!unverify 解除權限 \n a!verify <密碼>#開啟管理員權限 \n a!copy <數量>#備份當前頻道訊息\n a!clear <數量>備份當前頻道訊息 \n a!say<訊息>發送匿名訊息"
                )
                await message.channel.send(embed=ahelp)
        elif message.content.startswith("a!say"):  #can_you_say_that_again?
                tmp = message.content.split("a!say ", 2)
                if len(tmp) == 1:
                    await message.channel.send("缺參數")
                else:
                    await message.delete()
                    await message.channel.send(tmp[1])

        elif message.content.startswith("a!clear"):#刪除訊息
                clear = message.content.split(" ")
                if len(clear) <= 1:
                    await message.channel.send("缺參數")
                else:
                    clear[1]=int(clear[1])

                await message.channel.purge(limit=clear[1] + 1)
        #
        elif message.content.startswith('a!verify'):
            # 檢查用戶是否具有特定身分組
            user = message.author
            guild = message.guild
            await message.delete()
            # 檢查用戶是否在特定身分組中
            required_role = discord.utils.get(guild.roles, name=role_names[0])

            if required_role in user.roles:
                # 分割訊息，以獲取使用者輸入的密碼
                parts = message.content.split()
                
                if len(parts) >= 2:
                    password = parts[1]
                    #await message.delete()
                    # 檢查密碼是否正確（這裡示範一個簡單的密碼 "secret"）
                    if password == '12345678':
                        # 獲取伺服器中的身分組（根據名稱，請替換成身分組名稱）
                        role_0 = discord.utils.get(guild.roles, name=role_names[1])
                        if role_0:
                            # 將使用者添加到身分組
                            await user.add_roles(role_0)
                            await message.channel.send(f"{user.mention} 已成功加入身分組 {role_0.name}")
                            #await message.delete()
                        else:
                            await message.channel.send("找不到指定的身分組")
                    else:
                        await message.channel.send("密碼不正確")
                else:
                    await message.channel.send("請提供密碼，例如：`a!verify 密碼`")
            else:
                await message.channel.send("你必須擁有特定身分組才能使用此指令")
        elif message.content.startswith('a!unverify'):
        # 檢查用戶是否具有特定身分組
            user = message.author
            guild = message.guild
            await message.delete()

            # 檢查用戶是否在特定身分組中
            required_role = discord.utils.get(guild.roles, name=role_names[0])

            if required_role in user.roles:
                # 獲取伺服器中的身分組（根據名稱，請替換成身分組名稱）
                role_1 = discord.utils.get(guild.roles, name=role_names[1])

                if role_1:
                    # 將使用者從身分組中移除
                    await user.remove_roles(role_1)
                    await message.channel.send(f"{user.mention} 已從身分組 {role_1.name} 中移除")
                else:
                    await message.channel.send("找不到指定的身分組")
            else:
                await message.channel.send("你必須擁有特定身分組才能使用此指令")
        ##
        elif message.content.startswith('a!copy'):
            try:
                # 備份數量
                if len(message.content.split()) < 2:
                    await message.channel.send("請提供要備份的訊息數量")
                    return
                # 解析數量
                num_messages = int(message.content.split()[1])
                # 獲取歷史紀錄
                messages = []
                async for msg in message.channel.history(limit=num_messages):
                    messages.append(msg)
                # 取得時間
                current_datetime = datetime.datetime.now()             
                # 時間+文件名(文件創建)
                backup_filename = current_datetime.strftime("%Y%m%d%H%M%S") + "_message_backup.txt"
                # 創建txt保留備份
                with open(f"備份的訊息/{backup_filename}", "w", encoding="utf-8") as file:
                    for msg in reversed(messages):
                        if msg.attachments:
                            for attachment in msg.attachments:
                                file.write(f"{msg.author.display_name} sent an attachment: {attachment.url}\n")
                        else:
                            file.write(f"{msg.author.display_name}: {msg.content}\n")
                # 傳送備份文件
                with open(f"備份的訊息/{backup_filename}", "rb") as file:
                    await message.channel.send("以下是備份的訊息記錄：", file=discord.File(file, filename=backup_filename))
            except ValueError:
                await message.channel.send("請提供有效的訊息數量。")
            except Exception as e:
                await message.channel.send(f"備份訊息時出現錯誤：{e}")

        await client.process_commands(message)
client.run(
    cfg["bot_token"])
