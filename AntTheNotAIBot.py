import os
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks

import asyncio
from datetime import datetime as dt

load_dotenv(os.path.join(os.getcwd(), '.env'))
TOKEN = os.getenv('DISCORD_TOKEN') # taking discord bot token form .env file

# target_channel_id = os.getenv('MAIN_CHANNEL') # taking from .env
# target_channel_id = os.getenv('TEST_CHANNEL') 
target_channel_id = os.getenv('SPAM_CHANNEL') 

# course_name = "ML4Iot"
# print(target_channel_id)
# print(TOKEN)

bot = commands.Bot("!")


@tasks.loop(hours=24)
async def alarm():
    await bot.wait_until_ready() ## very important, or u get NoneType for Channel ID

    channel = bot.get_channel(int(target_channel_id))
    print(f"Got channel {channel}")

    for mins in range(10,0,-1):
        print(f'msg waiting to send (minUntilIdx:{mins})')
        await asyncio.sleep(60)
        
        await channel.send(f"TESTING, {mins}mins until MLIot, buckle up and rocket to the zoom!!!")
        # await channel.send(f"@here, {mins}mins until MLIot, buckle up and rocket to the zoom!!!")
        print(f'msg sent (minUntilIdx:{mins})')



@alarm.before_loop
async def before():
    targets = {
        # testing for different time w/ different day
        4: {
            "target": (23, 45, 00),
            "alias": "Friday"
        },
        #============================================

        1: {
            "target": (12, 50, 0), ## hour, mins, sec
            "alias": "Tuesday" #~ alias tag for future implementation 
        }, 

        3: {
            "target": (12, 50, 0),
            "alias": "Thursday"
        }
    }

    is_target = False
    
    while not is_target:
        today_day = dt.now().weekday()
        print(f'Today day: {today_day} (index).')

        if today_day in targets:
            print('Found target.')

            target = dt.now().replace(hour=targets[today_day]["target"][0], minute=targets[today_day]["target"][1], second=targets[today_day]["target"][2])
            print('Target is %s.'% str(target))

            wait_time = (target - dt.now()).total_seconds()

            if wait_time < 0:
                print('time has pased, waitng end of day')
                end_day = dt.now().replace(hour=23, minute=59, second=59)
                wait_time = (end_day - dt.now()).total_seconds() + 5.0
                
            print(f'Waiting for {wait_time}.')
            await asyncio.sleep(wait_time)
            is_target = True


        else:
            print ('No task for today, waiting for tomorrow.')
            await asyncio.sleep(43200) ## 12 hours in second
        

    await bot.wait_until_ready()
    print("Finished waiting.")


@bot.event
async def on_ready():
    print(f'{bot.user} is Online') # confirmed connection

@bot.listen('on_message') # use on_message to not block away the command from below
async def listen(message):
    if message.author == bot.user:
        return
    
    if 'No' in message.content:
        await message.channel.send("YES")

    if 'Yes' in message.content:
        await message.channel.send("NO")

    if "oh no" in message.content.lower():
        await message.channel.send("Oh YES")

    if "hell yeah" or "oh yes" in message.content.lower():
        await message.channel.send("HeeeeeLL No!!!")

    if "this is a loop" in message.content.lower():
        await message.channel.send("this is also a loop")        


@bot.command(name="ravioli") # call when there is cammand that matched
async def ravioli(ctx):
    await ctx.channel.send(file=discord.File('ravioli.gif'))
    await ctx.channel.send("\"Ravioli, Ravioli, what's in the pocket-oli?\"")


alarm.start()
bot.run(TOKEN)