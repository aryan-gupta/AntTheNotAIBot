import os
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks

import asyncio
from datetime import datetime as dt

load_dotenv(os.path.join(os.getcwd(), '.env'))
TOKEN = os.getenv('DISCORD_TOKEN') # taking discord bot token form .env file
target_channel_id = os.getenv('TARGET_CHANNELID') # taking from .env
# print(TOKEN)

bot = commands.Bot('!')

@tasks.loop(hours=1)
async def alarm():
    message_channel = bot.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    await message_channel.send("Your message")

@alarm.before_loop
async def before():
    targets = {
        1: {
            "target": (12, 50, 0),
            "alias": "Tuesday"
        }, 

        3: {
            "target": (12, 50, 0),
            "alias": "Thursday"
        },

        # testing 
        # 5: {
        #     "target": (2, 00, 00),
        #     "alias": "Friday"
        # }
    }

    is_target = False
    
    while not is_target:
        today_day = dt.now().weekday()

        print('today day')

        if today_day in targets:
            
            print('found target')
            target = dt.now().replace(hour=targets[today_day]["target"][0], minute=targets[today_day]["target"][1], second=targets[today_day]["target"][2])
            
            print('target is %s'% str(target))
            wait_time = (target - dt.now()).total_seconds()

            if wait_time < 0:
                print('time has pased, waitng end of day')
                end_day = dt.now().replace(hour=23, minute=59, second=59)
                wait_time = (end_day - dt.now()).total_seconds() + 5.0
                
            print(f'waiting for {wait_time}')
            await asyncio.sleep(wait_time)
            is_target = True


        else:
            print ('no task for today waiting for tomorrow')
            await asyncio.sleep(43200) # 12 hours
        

    await bot.wait_until_ready()
    print("Finished waiting")


# @bot.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')


alarm.start()

bot.run(TOKEN)