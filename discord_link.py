# discountGroovy.py
import os

import discord
#from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtubesearchpython import VideosSearch
import youtube_dl
import ffmpeg
import re

#load_dotenv()
TOKEN = 'ODg3NTc4OTY2OTE4MDUzOTQ5.YUGMVA.jJD-vBv0_sHlNQ3iC-KGlLg_GYw'

bot = commands.Bot(command_prefix='?')


@bot.command()
async def play(ctx, *args):
    msg = 'enjoy your shite song'
    
    url = args[0]

    # Checking if the url is a youtube link, if not then use youtubesearchpython
    if not re.match(r'.*www.youtube.*', url):
        # Join list into args
        url = ' '.join(args)
        tempSearch = VideosSearch(url, limit = 1)
        tempURL = tempSearch.result()['result'][0]['link']
        url = tempURL

    # Connect the bot to the channel
    channel = ctx.author.voice.channel
    await channel.connect()

    # Play the youtube audio, taken from stackoverflow
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

    voice.volume = 75
    
    voice.is_playing()

    await ctx.send(msg)

@bot.command()
async def stop(ctx):
    msg = "I really should stop playing shouldn't I?"
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send(msg)

@bot.command()
async def skip(ctx):
    msg = "Alright i'll skip this one"
    await ctx.send(msg)

@bot.command()
async def pause(ctx):
    msg = "Alright alright give me a fucking second"
    await ctx.send(msg)

    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.pause()

@bot.command()
async def resume(ctx):
    msg = "There you fucking go you mut"
    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.resume()

    await ctx.send(msg)

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    msg = "Aight see ya later cunt"
    await ctx.send(msg)



bot.run(TOKEN)



