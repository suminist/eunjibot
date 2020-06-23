import discord
from discord.ext import commands
import os
import random
from itertools import cycle
import json
from bs4 import BeautifulSoup as bSoup
import requests

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def goodnight(self, ctx):

        iuwu = [
            'https://tenor.com/view/iu-cute-hug-sleeping-gif-15049574',
            'https://tenor.com/view/iu-sleep-sleepy-sleeping-tired-gif-12177560'
        ]
        await ctx.send(random.choice(iuwu))

    @commands.command()
    async def whatslunch(self, ctx):

        lunch = [
            'Pasta',
            'Takeout',
            "Don't eat, have a snack instead",
            'Some fruits',
            'Mcdonalds'
        ]
        await ctx.send(random.choice(lunch))
    
    @commands.command()
    async def apink(self, ctx, *, msg):

        members= ['eunji', 'bomi', 'hayoung', 'naeun', 'namjoo', 'chorong']

        for mem in members:
            if str(msg.lower()) == mem:
                link = f'https://kprofiles.com/{msg}-profile-facts/'
                emb_title = 'Member Profile'

                source = requests.get(link).text
                soup = bSoup(source, 'lxml')

                kp_f = soup.find('div', class_='entry-content').p.text #print these facts

                kp_jpg = soup.find('div', class_='entry-content').img
                kp_src = kp_jpg['src'] #print this image

                embed_kp = discord.Embed(
                    title = emb_title,
                    color = 0x29FFCE
                )

                embed_kp.add_field(name='Info', value=kp_f)
                embed_kp.set_image(url=kp_src)
                embed_kp.add_field(name='Profile Link', value=link, inline=False)

                await ctx.send(embed=embed_kp)
                break

    @commands.command()
    async def izone(self, ctx, *, msg):

        izone = {
        'chaeyeon': 'https://kprofiles.com/lee-chaeyeon-izone-profile-facts/',
        'eunbi': 'https://kprofiles.com/kwon-eunbi-izone-profile-facts/',
        'sakura': 'https://kprofiles.com/miyawaki-sakura-izonehkt48-profile-facts/',
        'hyewon': 'https://kprofiles.com/kang-hyewon-izone-profile-facts/',
        'yena': 'https://kprofiles.com/choi-yena-izone-profile-facts/',
        'chaewon': 'https://kprofiles.com/kim-chaewon-profile-facts/',

        'minjoo': 'https://kprofiles.com/kim-minjoo-izone-profile-facts/',
        'minju': 'https://kprofiles.com/kim-minjoo-izone-profile-facts/',
        
        'nako': 'https://kprofiles.com/yabuki-nako-izonehkt48-profile-facts/',
        'hitomi': 'https://kprofiles.com/honda-hitomi-izoneakb48-profile-facts/',
        'yuri': 'https://kprofiles.com/jo-yuri-izone-profile-facts/',
        'yujin': 'https://kprofiles.com/ahn-yujin-izone-profile-facts/',
        'wonyoung': 'https://kprofiles.com/jang-wonyoung-izone-profile-facts/'
        }

        link = izone.get(msg.lower())

        if link == None:
            await ctx.send('Oops, maybe spelt something wrong?') 
        
        else:
            emb_title = 'Member Profile'

            source = requests.get(link).text
            soup = bSoup(source, 'lxml')

            kp_f = soup.find('div', class_='entry-content').p.text #print these facts

            kp_jpg = soup.find('div', class_='entry-content').img
            kp_src = kp_jpg['src'] #print this image

            embed_kp = discord.Embed(
                title = emb_title,
                color = 0xD609DD
            )

            embed_kp.add_field(name='Info', value=kp_f)
            embed_kp.set_image(url=kp_src)
            embed_kp.add_field(name='Profile Link', value=link, inline=False)    

            await ctx.send(embed=embed_kp)

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(
            title = 'List of Commands',
            description = 'Bot Prefix: -',
            color = 0x65E1F0
        )
        embed.add_field(name='emb1', value='Posts Jeong Eunji', inline=False)
        embed.add_field(name='form1', value='Sends you a little form', inline=False)
        embed.add_field(name='goodnight', value='Sends you 1 out of 2 goodnight gif', inline=False)
        embed.add_field(name='latestcb', value='Sends the latest girl/girl group comeback', inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'Message from {message.author.id} in channel {message.channel.id} in server {message.guild.id}')
        print(message.content)

        splt = str(message.author.display_name) #nickname
        # tag_id = str(message.author.id)         #discord ID
        msg_n = message.content.lower()    #message.content

        if 'is high' in msg_n: #easter egg
            await message.channel.send('https://www.youtube.com/watch?v=fpSTrry_5Fo')
            
        elif 'i love you eunji' in msg_n:
            await message.channel.send(f'i love you too {splt} :flushed:')
            await message.add_reaction('\N{HEAVY BLACK HEART}') 
            
        elif 'depressed' in msg_n:
            await message.channel.send(f"its ok {splt}, I'll be there for you")
            await message.channel.send('<:eunjiface:707716555538038875>')

        elif 'hug me' in msg_n:
            await message.channel.send(f'*hugs {splt}*')
            await message.channel.send('<:pandahug:707726416065593355>')

        elif 'thanks eunji' in msg_n:
            await message.channel.send(f"you're welcome {splt} :)")

        elif '<@!707455402744217610>' in msg_n:
            await message.channel.send("I'm busy right now :/ ping me again later")

        elif 'sing' in msg_n and 'eunji' in msg_n:
            videos = [
                'https://www.youtube.com/watch?v=nzDO6tAB6ng',
                'https://www.youtube.com/watch?v=PWDISJZr7Yc',
                'https://www.youtube.com/watch?v=tUUk7ktOy4Y',
                'https://www.youtube.com/watch?v=S20j3sTDZT0',
                'https://www.youtube.com/watch?v=ugh3W-D-tqk',
                'https://www.youtube.com/watch?v=otrquLJGX6c'
            ]
            await message.channel.send(random.choice(videos))

    @commands.Cog.listener()
    async def on_ready(self):
        print('<<<<<=====<>=====<>=====Eunjibot Online=====<>=====<>=====>>>>>')
