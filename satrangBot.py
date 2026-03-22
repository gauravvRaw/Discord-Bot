import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import berserk
from PIL import Image
import requests
import io

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
lichess_token = os.getenv('LICHESS_TOKEN')
session = berserk.TokenSession(lichess_token)
client1 = berserk.Client(session=session)

intents = discord.Intents.default() 
bot = commands.Bot("!", intents= intents)


def bonk_generator(image):
    overlay = image
    frames = []
    background0 = Image.open("backdrop.png")
    bonk1 = Image.open("frame_1.png")
    background0.paste(overlay, (320, 260), mask = overlay)
    background0.paste(bonk1, (25,50), mask = bonk1)  
    background0 = background0.resize((100,100))
    frames.append(background0)

    background1 = Image.open("backdrop.png")
    bonk2 = Image.open("frame_2.png")
    background1.paste(overlay, (320, 260), mask = overlay)
    background1.paste(bonk2, (25,50), mask = bonk2)
    background1 = background1.resize((100,100))
    frames.append(background1)
    frames.append(background1)
    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    buffer.seek(0)
    return buffer

# COMMANDS AND EVENTS HERE ON
@bot.command()
async def bonk(ctx, *, member: discord.Member):
    url =  member.display_avatar.url
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
    bonk_ = bonk_generator(img)
    await ctx.send(file=discord.File(bonk_, filename="bonk.gif"))

@bot.command()
async def pfp(ctx, *, member: discord.Member):
    embed = discord.Embed(title=f"{member} ki photu")
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)    

@bot.command()
async def fry(ctx, *, member: discord.Member):
    url =  member.display_avatar.url
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    out = img.point(lambda i: i * 5)
    buffer = io.BytesIO()
    out.save(buffer, format="PNG")
    buffer.seek(0)

    await ctx.send(file=discord.File(buffer, filename="out.png"))

@bot.command()
async def safai(ctx, num: int):
    if(num > 50):
        await ctx.send("chup be")
        return
    await ctx.channel.purge(limit=num)

@bot.command()
async def chess(ctx):
    chal = client1.challenges.create_open()
    link = chal["url"]
    await ctx.send(link)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if ("satrangi") in message.content.lower():
        await message.channel.send("JINDAA ")
    await bot.process_commands(message) 

intents.message_content = True
intents.members = True

bot.run(token)
