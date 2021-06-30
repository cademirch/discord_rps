import discord
import asyncio
import async_timeout
import dotenv
import os
from db import Database
from discord.ext import commands
from collections.abc import Sequence

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
ACCEPTABLE_MOVES = ['rock', 'paper', 'scissors']

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def challenge(ctx, user: discord.Member):   
    user1, user2 = ctx.author, user
    
    db = Database()
    db.add_user(user1.id, user2.id)
    
    if str(user.status) == "offline":
        await ctx.send(f"{user.mention} is not online!")
        return
    elif str(user.status) == "online":
        await ctx.send(f"{ctx.author.mention} challenged {user.mention}! You both have 10 seconds to DM me your move!")
        
        r1, r2 = None, None
        
        try:
            async with async_timeout.timeout(10.0):
                r1 = await bot.wait_for('message', check=message_check(channel=user1.dm_channel))
                r2 = await bot.wait_for('message', check=message_check(channel=user2.dm_channel))
        except(asyncio.TimeoutError, asyncio.CancelledError):
            if r1 is None and r2 is None:
                await ctx.send(f"{user1.mention} and {user2.mention} did not respond in time. They both lose.")
                db.update_losses(user1.id, user2.id)
                return
            elif r1 is None and r2 is not None:
                await ctx.send(f"{user1.mention} did not respond in time. They lose.")
                db.update_win_loss(user2.id, user1.id)
                return
            elif r2 is None and r1 is not None:
                await ctx.send(f"{user2.mention} did not respond in time. They lose.")
                db.update_win_loss(user1.id, user2.id)
                return
        if r1.content.lower() not in ACCEPTABLE_MOVES:
            await ctx.send(f"{user1.mention} did not respond with a proper move. What an idiot. They lose.")
            db.update_win_loss(user2.id, user1.id)
            return
        elif r2.content.lower() not in ACCEPTABLE_MOVES:
            await ctx.send(f"{user2.mention} did not respond with a proper move. What an idiot. They lose.")
            db.update_win_loss(user1.id, user2.id)
            return
        

dotenv.load_dotenv()
bot.run(os.getenv('TOKEN'))