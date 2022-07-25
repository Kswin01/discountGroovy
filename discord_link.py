# discountGroovy.py
import os
import asyncio

import discord
#from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtubesearchpython import VideosSearch
import time
import youtube_dl
import ffmpeg
import re


#load_dotenv()
TOKEN = 'enter token here'

bot = commands.Bot(command_prefix='?')


music_queue = []

async def music_player(ctx):

    while len(music_queue) >= 0:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice.is_playing() is True:
            await asyncio.sleep(10)
            continue
        elif len(music_queue) == 0:
            await dc(ctx)
            return

        curr_ctx = ctx
 
        url = music_queue.pop(0)
        if url == "https://www.youtube.com/watch?v=ZCBz8A0Sx_8":
            await ctx.send("Whilst i do agree, no")
            await asyncio.sleep(10)
            continue
        # Play the youtube audio, taken from stackoverflow
 
        ydl_opts = {
            'format': 'worst',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Checking to make sure that the video is under 10 minutes in length
            dictMeta = ydl.extract_info(url, download=False)
            
            vid_length = dictMeta['duration']

            if vid_length > 600:
                msg = 'the fuck u think u doing eh?'
                await ctx.send(msg)
                return

            ydl.download([url])


        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio("song.mp3"))

        voice.volume = 75

        voice.is_playing()
        msg = "Now playing " + url
        
        await ctx.send(msg)

        await asyncio.sleep(10)

@bot.command()
async def skip(ctx):
    if len(music_queue) == 0:
        await ctx.send("No songs in the queue")
    else:
        voice = get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await music_player(ctx)

@bot.command()
async def play(ctx, *args):    
    url = args[0]

    # Checking if the url is a youtube link, if not then use youtubesearchpython
    if not re.match(r'.*www.youtube.*', url):
        # Join list into args
        url = ' '.join(args)
        tempSearch = VideosSearch(url, limit = 1)
        tempURL = tempSearch.result()['result'][0]['link']
        url = tempURL

    # Connect the bot to the channel if it is not already
    if ctx.guild.voice_client not in bot.voice_clients:
        channel = ctx.author.voice.channel
        await channel.connect()


    # Add the url to the music queue
    music_queue.append(url)
    
    msg = "Added " + url + " to the queue"

    if len(music_queue) == 0:
        await ctx.send("Queue is empty")
        return
   
    await ctx.send(msg)

    await music_player(ctx)


def start_playing(voice_client, player):

    music_queue[0] = player

    i = 0
    while i <  len(music_queue):
        try:
            voice_client.play(music_queue[i], after=lambda e: print('Player error: %s' % e) if e else None)

        except:
            pass
        i += 1


@bot.command()
async def stop(ctx):
    msg = "I really should stop playing shouldn't I?"
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    music_queue.clear()
    await ctx.send(msg)

@bot.command()
async def pause(ctx):
    msg = "Pausing"
    await ctx.send(msg)

    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.pause()

@bot.command()
async def resume(ctx):
    msg = "Resuming"
    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.resume()

    await ctx.send(msg)

@bot.command()
async def dc(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    music_queue.clear()
    msg = "Bye Bye!"
    await ctx.send(msg)

@bot.command()
async def queue(ctx):
    await ctx.send(music_queue)

bot.run(TOKEN)



