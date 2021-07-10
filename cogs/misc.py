import discord
from discord.ext import commands, tasks
import os
import random
from itertools import cycle
import json
from bs4 import BeautifulSoup as bSoup
import requests
import time
import operator
from functools import reduce
from datetime import datetime, date, timedelta
import pytz
import traceback
import asyncio

from secret_keys import MONGODB_CONNECTION

import pymongo
cluster = pymongo.MongoClient(MONGODB_CONNECTION)


class MiscCog(commands.Cog):
    """
    Miscellaneous stuff that leek likes
    """

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Miscellaneous"
        self.krupdate_loop.start()

    @commands.command()
    @commands.guild_only()
    async def goodnight(self, ctx):

        iuwu = [
            'https://tenor.com/view/iu-cute-hug-sleeping-gif-15049574',
            'https://tenor.com/view/iu-sleep-sleepy-sleeping-tired-gif-12177560'
        ]
        await ctx.send(random.choice(iuwu))
        
    @commands.command()
    @commands.guild_only()
    async def admin(self, ctx, *args):
        if args[0] == "command":
            if args[1] == "001":
                await ctx.send(f"Hello {ctx.author.name}, please specify nuclear launch codes to proceed.")

    @commands.command()
    @commands.guild_only()
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
    @commands.guild_only()
    async def apink(self, ctx, *, msg):

        members = ['eunji', 'bomi', 'hayoung', 'naeun', 'namjoo', 'chorong']

        for mem in members:
            if str(msg.lower()) == mem:
                link = f'https://kprofiles.com/{msg}-profile-facts/'
                emb_title = 'Member Profile'

                source = requests.get(link).text
                soup = bSoup(source, 'lxml')

                # print these facts
                kp_f = soup.find('div', class_='entry-content').p.text

                kp_jpg = soup.find('div', class_='entry-content').img
                kp_src = kp_jpg['src']  # print this image

                embed_kp = discord.Embed(
                    title=emb_title,
                    color=0x29FFCE
                )

                embed_kp.add_field(name='Info', value=kp_f)
                embed_kp.set_image(url=kp_src)
                embed_kp.add_field(name='Profile Link',
                                   value=link, inline=False)

                await ctx.send(embed=embed_kp)
                break

    @commands.command()
    @commands.guild_only()
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

            # print these facts
            kp_f = soup.find('div', class_='entry-content').p.text

            kp_jpg = soup.find('div', class_='entry-content').img
            kp_src = kp_jpg['src']  # print this image

            embed_kp = discord.Embed(
                title=emb_title,
                color=0xD609DD
            )

            embed_kp.add_field(name='Info', value=kp_f)
            embed_kp.set_image(url=kp_src)
            embed_kp.add_field(name='Profile Link', value=link, inline=False)

            await ctx.send(embed=embed_kp)

    @commands.command()
    @commands.guild_only()
    async def helpme(self, ctx):
        embed = discord.Embed(
            title='List of Commands',
            description='Bot Prefix: -',
            color=0x65E1F0
        )
        embed.add_field(name='emb1', value='Posts Jeong Eunji', inline=False)
        embed.add_field(
            name='form1', value='Sends you a little form', inline=False)
        embed.add_field(
            name='goodnight', value='Sends you 1 out of 2 goodnight gif', inline=False)
        embed.add_field(
            name='latestcb', value='Sends the latest girl/girl group comeback', inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        #print(f'Message from {message.author.id} in channel {message.channel.id} in server {message.guild.id}')
        # print(message.content)

        splt = str(message.author.display_name)  # nickname
        # tag_id = str(message.author.id)         #discord ID
        msg_n = message.content.lower()  # message.content

        if 'is high' in msg_n:  # easter egg
            await message.channel.send('https://www.youtube.com/watch?v=fpSTrry_5Fo')
        elif 'the best girl' in msg_n:
            await message.channel.send("It's me", delete_after=1)
        elif 'i love you eunji' in msg_n:
            await message.channel.send(f'i love you too {splt} :flushed:')
            await message.add_reaction('\N{HEAVY BLACK HEART}')

        elif 'depressed' in msg_n:
            await message.channel.send(f"its ok {splt}, I'll be there for you")
            await message.channel.send('<:eunjiface:707716555538038875>')

        elif 'hug me' in msg_n:
            if message.author.id == 382915421071736852:
                await message.channel.send(f'*kisses {splt}*')
            else:
                await message.channel.send(f'*hugs {splt}*')

            await message.channel.send('<:pandahug:707726416065593355>')

        elif 'thanks eunji' in msg_n:
            await message.channel.send(f"you're welcome {splt} :)")

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

    @commands.command()
    @commands.guild_only()
    async def opgg(self, ctx, *, summoner):

        msgn = str(summoner)

        op_gg = msgn.split()

        if len(op_gg) > 1:
            username = msgn.replace(' ', '+')

        elif len(op_gg) == 1:
            username = msgn

        else:
            pass

        url = f'https://na.op.gg/summoner/userName={username}'

        try:
            source = requests.get(url).text
            soup = bSoup(source, 'lxml')
            meow = soup.find('h2', class_='Title').text
        except:
            meow = 'nothing'

        if meow == 'This summoner is not registered at OP.GG. Please check spelling.':
            await ctx.send('Please enter a valid summoner name')
        else:
            message = await ctx.send(url)
            await message.add_reaction('\N{White Heavy Check Mark}')
            await message.add_reaction('\N{Cross Mark}')

    @tasks.loop(seconds=1)
    async def krupdate_loop(self):
        try:
            print("start kr loop")
            await pause_until(self._kr_next_update_dt)

            db = cluster['minjubot']
            krbot = db['hyewonfragrant']

            channels = [self.bot.get_channel(
                723401657148244009), self.bot.get_channel(743562872025514075), self.bot.get_channel(564352023928242186)]
            url = 'https://www.koreanclass101.com/korean-phrases/'
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}
            source = requests.get(url, headers=headers).text
            soup = bSoup(source, 'lxml')

            wode = soup.find('div', class_='r101-wotd-widget__english').text

            wtd = []
            ix = krbot.find({'index': 'qfind'})

            for item in ix:
                wtd.append(item['krword'])
            twod = ''.join(wtd)

            today = date.today()
            wodxa = soup.find_all('div', class_='r101-wotd-widget__word')
            wodexa = soup.find_all('div', class_='r101-wotd-widget__english')
            ewords = []
            for eng in wodexa:
                ewords.append(eng.get_text())
            ewords = ["||" + item + "||" for item in ewords]
            kwords = []
            for kor in wodxa:
                kwords.append(kor.get_text())

            xlst = list(reduce(operator.add, zip(ewords, kwords)))

            carrot = ''
            for xls in range(len(xlst)):
                if xls % 2 == 0:
                    nls = xls - 2
                    blist = ' - '.join(xlst[nls:xls])
                    if blist == '':
                        pass
                    else:
                        carrot += f'{blist}\n'

            for channel in channels:
                await channel.send(f"```css\n{today} - Korean word of the day with examples```")
                await channel.send(carrot)
            if twod == '':
                newvalues = {'index': 'qfind', 'krword': wode}
                krbot.insert_one(newvalues)
            else:
                query = {'index': 'qfind'}
                krbot.update_one(query, {'$set': {'krword': wode}})

            while self._kr_next_update_dt < datetime.utcnow().replace(tzinfo=pytz.utc):
                self._kr_next_update_dt += timedelta(days=1)

        except Exception as e:
            traceback.print_exc()

    @krupdate_loop.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()
        self._kr_next_update_dt = datetime(2020, 7, 17, 15, 3, 0, 0, pytz.utc)

        while self._kr_next_update_dt < datetime.utcnow().replace(tzinfo=pytz.utc):
            self._kr_next_update_dt += timedelta(days=1)

    @commands.command()
    @commands.guild_only()
    async def krupdate(self, ctx):
        db = cluster['minjubot']
        krbot = db['hyewonfragrant']

        url = 'https://www.koreanclass101.com/korean-phrases/'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}
        source = requests.get(url, headers=headers).text
        soup = bSoup(source, 'lxml')

        wode = soup.find('div', class_='r101-wotd-widget__english').text

        wtd = []
        ix = krbot.find({'index': 'qfind'})

        for item in ix:
            wtd.append(item['krword'])
        twod = ''.join(wtd)

        if twod == wode:
            await(await ctx.send("Already updated")).delete(delay=3)
        else:
            today = date.today()
            await ctx.send(f"```css\n{today} - Korean words of the day with examples```")
            wodxa = soup.find_all('div', class_='r101-wotd-widget__word')
            wodexa = soup.find_all('div', class_='r101-wotd-widget__english')
            ewords = []
            for eng in wodexa:
                ewords.append(eng.get_text())
            ewords = ["||" + item + "||" for item in ewords]
            kwords = []
            for kor in wodxa:
                kwords.append(kor.get_text())

            xlst = list(reduce(operator.add, zip(ewords, kwords)))

            carrot = ''
            for xls in range(len(xlst)):
                if xls % 2 == 0:
                    nls = xls - 2
                    blist = ' - '.join(xlst[nls:xls])
                    if blist == '':
                        pass
                    else:
                        carrot += f'{blist}\n'

            await ctx.send(carrot)

            if twod == '':
                newvalues = {'index': 'qfind', 'krword': wode}
                krbot.insert_one(newvalues)
            else:
                query = {'index': 'qfind'}
                krbot.update_one(query, {'$set': {'krword': wode}})

        await ctx.message.delete()


async def pause_until(dt):

    end = dt.timestamp()
    # Now we wait
    while True:
        now = datetime.utcnow().replace(tzinfo=pytz.utc).timestamp()
        diff = end - now

        #
        # Time is up!
        #
        if diff <= 0:
            break
        else:
            # 'logarithmic' sleeping to minimize loop iterations
            await asyncio.sleep(diff / 2)
