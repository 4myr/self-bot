# Self bot | You can login to this bot with your account and enjoy from services!

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import logging, config, sys, getpass, asyncio
import psutil, random
import json, requests, os

instance =  input('Enter your instance name [example: amyr]: ') if len(sys.argv) < 2 else sys.argv[1]

# A simply function for showing errors
def throwError(error):
    print("[Error]: ", error)

# A simply function to making link for a user
def linkToUser(from_id, name):
    link = "[{}](tg://user?id={})".format(name, from_id)
    return link

# Telethon client start
client = TelegramClient(instance, config.api_id, config.api_hash)
print("Self is running now...")
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)

# An event to handle new messages
@client.on(events.NewMessage)
async def newMessage(event):

    if hasattr(event.to_id, 'chat_id'):
        to_id = event.to_id.chat_id
    elif hasattr(event.to_id, 'user_id'):
        to_id = event.to_id.user_id
    elif hasattr(event.to_id, 'channel_id'):
        to_id = event.to_id.channel_id
    cmd_message = str(event.raw_text)
    splited_cmd_message = cmd_message.split(' ', 2)
    me = await client.get_me()

# Self commands
    if cmd_message == '!selfhelp':
        helpText = """**📍 راهنمای دستورات سلف :**
➖➖
!ping
💭 بررسی آنلاین بودن ربات

!me
💭 ارسال اطلاعات عمومی اکانت

!animchar [loop] [char]
💭 لوپ چند شکلک به ترتیب

!heart [loop]
💭 لوپ شکلک های قلبی

!smile [loop]
💭 لوپ شکلک های خنده

!id [reply]
💭 ارسال اطلاعات یک اکانت با ریپلای

!mention [max] [text]
💭 منشن کردن اعضای آنلاین گروه

!flood [loop]
💭 ارسال اسپم به تعداد دلخواه

!stats
💭 ارسال آمار اکانت
"""
        await event.edit(helpText)

    # Show myself information
    if cmd_message == '!ping':
        userLink = linkToUser(me.id, me.first_name)
        resultText = "**Self bot is online** 🐍\n\n**RAM Usage: %{}**\n**CPU Usage: %{}**\n**Disk Usage: %{}**\n\n{}".format(psutil.virtual_memory()[2], psutil.cpu_percent(), psutil.disk_usage('/')[3], userLink)
        await event.edit(resultText)

    # Show myself information
    if cmd_message == '!me':
        resultText = "i'm {} with user_id: {}".format(me.first_name, me.id)
        await event.edit(resultText)
    
    # Show replied account information
    if cmd_message == '!id' or cmd_message == 'سلام' or cmd_message == 'خ':
        rep = await event.get_reply_message()
        if rep:
            sender = rep.sender
            username = "@{}".format(sender.username) if sender.username != None else None
            userLink = linkToUser(sender.id, sender.first_name)
            resultText = "First Name: {}\nLast Name: **{}**\nFrom ID: **{}**\nUsername: **{}**".format(userLink, sender.last_name, sender.id, username)
            await client.send_message(me.id, resultText)
            if cmd_message == '!id':
                await event.edit(resultText)
            if cmd_message == 'خ':
                await event.delete()
        
    # Mentions online users
    if splited_cmd_message[0] == '!mention' and hasattr(event.to_id, 'channel_id') and splited_cmd_message[1].isdigit() and len(splited_cmd_message) == 3:
        mentions = str(splited_cmd_message[2])
        users = await client.get_participants(event.to_id.channel_id, limit=int(splited_cmd_message[1])+1)
        for user in users:
            if user.username is not None:
                mentions += "@{} ".format(user.username)

        await event.delete()
        await event.respond(mentions)

    # Show replied account information
    if cmd_message == '!setanswer' and splited_cmd_message[1] != None: 
        rep = await event.get_reply_message()
        sender = rep.from_id
        sender_text = rep.message
        await event.edit("{} {}".format(sender, sender_text))

    # Flood by specific count
    if splited_cmd_message[0].lower() == '!flood' and splited_cmd_message[1].isdigit():
        loop_time = int(splited_cmd_message[1])
        text_flood = splited_cmd_message[2]

        await event.delete()

        for i in range(loop_time):
            await event.respond(text_flood)
                    
    # Animate a specific message
    if splited_cmd_message[0].lower() == '!animchar' and splited_cmd_message[1].isdigit() and len(splited_cmd_message) == 3:
        loop_time = int(splited_cmd_message[1])
        repetition_txt = splited_cmd_message[2]

        message = await event.edit(repetition_txt)
        for i in range(loop_time):
            for j in range(len(repetition_txt)):
                if repetition_txt[j] != ' ':
                    await asyncio.sleep(0.5)
                    await client.edit_message(message, repetition_txt[0:j+1])
                    
    # Animate heart emojies
    if splited_cmd_message[0].lower() == '!heart' and splited_cmd_message[1].isdigit():
        loop_time = int(splited_cmd_message[1])

        emojies = ["❤️", "💋", "😘", "😂"]

        message = await event.edit("😍")
        for i in range(loop_time):
            for emoji in emojies:
                await asyncio.sleep(0.5)
                await client.edit_message(message, emoji)

    # Animate smile emojies
    if splited_cmd_message[0].lower() == '!smile' and splited_cmd_message[1].isdigit():
        loop_time = int(splited_cmd_message[1])

        emojies = ["😅", "😄", "🤣"]

        message = await event.edit("🤩")
        for i in range(loop_time):
            for emoji in emojies:
                await asyncio.sleep(0.3)
                await client.edit_message(message, emoji)

    # Show account stats
    if cmd_message == '!stats':
        await event.edit('**My stats is loading...**')
        dialogs = await client.get_dialogs()
        count_all = 0
        count_users = 0
        count_groups = 0
        count_channels = 0
        count_bots = 0
        for d in dialogs:
            count_all += 1
            if d.is_user:
                if d.entity.bot:
                    count_bots += 1
                else:
                    count_users += 1
            elif d.is_group:
                count_groups += 1
            elif d.is_channel:
                count_channels += 1

        resultText = "**My Stats**\n\nUsers: `{}`\nGroups: `{}`\nChannels: `{}`\nBots: `{}`\nAll: `{}`\n\n**RAM Usage: %{}**\n**CPU Usage: %{}**\n**Disk Usage: %{}**".format(count_users, count_groups, count_channels, count_bots, count_all, psutil.virtual_memory()[2], psutil.cpu_percent(), psutil.disk_usage('/')[3])
        await event.edit(resultText)
        
try:
    client.start()
    client.run_until_disconnected()
except Exception as error:
    throwError(error)