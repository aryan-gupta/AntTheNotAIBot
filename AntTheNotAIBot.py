import os
import discord
from dotenv import load_dotenv

from discord.ext import commands, tasks

import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
import time
import sched


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.AutoShardedBot(commands.when_mentioned_or("!"), help_command=None)

alarm_time = '19:50' #24hrs
now = datetime.now()
current_time = now.strftime("%H:%M")

@client.event
async def on_ready():
    print(f'{client.user.name} Online.')



@tasks.loop(seconds=1)
async def check_eachsec():
    message_channel = client.get_channel(os.getenv('TARGET_CHANNELID'))
    if current_time == alarm_time:
        print(f"Channel reminder sent, {message_channel}")
        await message_channel.send("Testing 101")
    else:
        pass


@check_eachsec.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")


@client.command()
async def remind(ctx, time: int, *, msg):
    while True:
        await sleep(time)
        await ctx.send(f'{msg}, {ctx.author.mention}')

check_eachsec.start()
client.run(TOKEN)
