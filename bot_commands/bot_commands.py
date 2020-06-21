import discord
from discord.ext import commands
import os
import random
from itertools import cycle
import json
from bs4 import BeautifulSoup as bSoup
import requests

from .lastfm import LastFM

class BotCommands:
    def __init__(self, client):

        self.command_list = [
            GoodNight(),
            WhatsLunch(),
            Ban(),
            Apink(),
            Izone(),
            HelpMe(),
            LastFM()
        ]
        
        for command in self.command_list:
            client.add_command(command)
            print(f"Loaded {command.name}")

        print('Finished loading all bot_commands')

        client.get_command('help').enabled = False

class GoodNight(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'goodnight'

    async def function(self, ctx):

        iuwu = [
            'https://tenor.com/view/iu-cute-hug-sleeping-gif-15049574',
            'https://tenor.com/view/iu-sleep-sleepy-sleeping-tired-gif-12177560'
        ]
        await ctx.send(random.choice(iuwu))

class WhatsLunch(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'whatslunch'

    async def function(self, ctx):

        lunch = [
            'Pasta',
            'Takeout',
            "Don't eat, have a snack instead",
            'Some fruits',
            'Mcdonalds'
        ]

        await ctx.send(random.choice(lunch))

class Ban(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'ban'

    async def function(self, ctx):
        await ctx.send('Please add a user ID in order to execute the command')

class Apink(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'apink'

    async def function(self, ctx, *, msg):

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

class Izone(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'izone'

    async def function(self, ctx, *, msg):

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

class HelpMe(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'helpme'
    
    async def function(self, ctx):
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
