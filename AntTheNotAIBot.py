import os
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks

import asyncio
from asyncio import sleep
import time, schedule


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # taking discord bot token form .env file

client = commands.AutoShardedBot(commands.when_mentioned_or("!"), help_command=None)

@client.event
async def on_ready():
    print(f'{client.user.name} Online.')


async def alarm():
    message_channel = client.get_channel(os.getenv('TARGET_CHANNELID')) # taking channelID form .env file
    print(f"Channel reminder sent, {message_channel}")
    await message_channel.send("Testing 101")

schedule.every().thursday.at("22:18").do(alarm)


while True:
    schedule.run_pending()
    time.sleep(1)




@client.command()
async def remind(ctx, time: int, *, msg):
    while True:
        await sleep(time)
        await ctx.send(f'{msg}, {ctx.author.mention}')

client.run(TOKEN)
