# bot.py
import os

import discord
#from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import ffmpeg

#load_dotenv()
TOKEN = 'ODg3NTc4OTY2OTE4MDUzOTQ5.YUGMVA.jJD-vBv0_sHlNQ3iC-KGlLg_GYw'

bot = commands.Bot(command_prefix='?')


@bot.command()
async def play(ctx, url):
    msg = 'I really should be playing something here'
    
    channel = ctx.author.voice.channel
    await channel.connect()

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'worst',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()

    await ctx.send(url)

@bot.command()
async def stop(ctx):
    msg = "I really should stop playing shouldn't I?"
    await ctx.send(msg)

@bot.command()
async def skip(ctx):
    msg = "Alright i'll skip this one"
    await ctx.send(msg)

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    msg = "Aight see ya later cunt"
    await ctx.send(msg)



bot.run(TOKEN)



