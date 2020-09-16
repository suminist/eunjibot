from datetime import datetime, timedelta
from urllib.parse import quote
import discord
from discord.ext import commands
import requests
import json
from secret_keys import LF_API_KEY, LF_API_SECRET
from db import users

import discord
from discord.ext import commands

class LastFmCog(commands.Cog):
    """
    LastFM stuff
    """
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "LastFM"

    @commands.command(aliases=['lf'])
    async def lastfm(self, ctx, *args):
        mentioned_users = ctx.message.mentions
        for mentioned_user in mentioned_users:
            ctx.message.content = ctx.message.content.replace(mentioned_user.mention, '')
            args = tuple(x for x in args if x != mentioned_user.mention)

        if len(args) == 0:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._now_playing(ctx, args[1:], user)
        elif args[0] in ['ta', 'topartists']:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._top_artists(ctx, args[1:], user)
        elif args[0] in ['tt', 'toptracks']:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._top_tracks(ctx, args[1:], user)
        elif args[0] in ['talb', 'topalbums']:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._top_albums(ctx, args[1:], user)
        elif args[0] in ['recent']:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._recent_tracks(ctx, args[1:], user)
        elif args[0] in ['np', 'nowplaying']:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._now_playing(ctx, args[1:], user)         
        elif args[0] in ['set']:
            await self._set_username(ctx, args[1:]) 
        else:
            if len(mentioned_users) == 0:
                user = ctx.author
            else:
                user = mentioned_users[0]
            await self._now_playing(ctx, args[1:], user)          

    async def _top_artists(self, ctx, args, user):
        username = await users.db_get_lf_username(user.id)

        if username == None:
            await ctx.send('Please register your username with `lf set username`')
            return
        
        if len(args) > 0:
            period = _lf_period(args[0])
        else:
            period = 'overall'

        embed = _embed_ta(username=username, page=1, period=period)
        message = await ctx.send(embed=embed)
        await _add_lf_emojis(message)

    async def _top_tracks(self, ctx, args, user):
        username = await users.db_get_lf_username(user.id)

        if username == None:
            await ctx.send('Please register your username with `lf set username`')
            return
        
        if len(args) > 0:
            period = _lf_period(args[0])
        else:
            period = 'overall'

        embed = _embed_tt(username=username, page=1, period=period)
        message = await ctx.send(embed=embed)
        await _add_lf_emojis(message)

    async def _top_albums(self, ctx, args, user):
        username = await users.db_get_lf_username(user.id)

        if username == None:
            await ctx.send('Please register your username with `lf set username`')
            return

        if len(args) > 0:
            period = _lf_period(args[0])
        else:
            period = 'overall'

        embed = _embed_talb(username=username, page=1, period=period)
        message = await ctx.send(embed=embed)
        await _add_lf_emojis(message)

    async def _recent_tracks(self, ctx, args, user):
        username = await users.db_get_lf_username(user.id)

        if username is None:
            await ctx.send('Please register your username with `lf set username`')
            return
        
        embed = _embed_recent(username=username, page=1)
        message = await ctx.send(embed=embed)
        await _add_lf_emojis(message)

    async def _now_playing(self, ctx, args, user):
        username = await users.db_get_lf_username(user.id)

        if username is None:
            await ctx.send('Please register your username with `lf set username`')
            return

        embed = _embed_np(username=username)
        await ctx.send(embed=embed)

    async def _set_username(self, ctx, args):
        if len(args) == 0:
            await ctx.send('Please include username `lf set username`')
            return

        author_id = ctx.message.author.id
        username = args[0]

        await users.db_set_lf_username(author_id, username)
        await ctx.send(f"Set username to {username}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            if "Last.fm" not in str(reaction.message.embeds[0].footer):
                return
        except:
            return

        author_field = reaction.message.embeds[0].author.name

        if 'currently listening' in author_field:
            return
        if 'last listened' in author_field:
            return
 
        if reaction.emoji == '⬅' and reaction.count > 1:
            action = 0
            await reaction.remove(user)
        elif reaction.emoji == '➡' and reaction.count > 1:
            action = 1
            await reaction.remove(user)
        elif reaction.emoji == '❌' and reaction.count > 1:
            action = 2
        else:
            return

        cur_page = int(reaction.message.embeds[0].footer.text.split(' ')[1].split('/')[0])
        max_page = int(reaction.message.embeds[0].footer.text.split(' ')[1].split('/')[1])

        if action == 0:
            new_page = cur_page - 1
        elif action == 1:
            new_page = cur_page + 1
        elif action == 2:
            await reaction.message.delete()
            return

        if new_page == 0:
            new_page = max_page
        elif new_page > max_page:
            new_page = 1

        username = author_field.split(' ')[0][:-2]

        if 'Recent Tracks' in author_field:
            embed = _embed_recent(username, new_page)
            await reaction.message.edit(embed=embed)
            return

        period = author_field.split(' ')[-3]

        if author_field.split(' ')[-1] == 'Artists':
            embed = _embed_ta(username, period, new_page)
            await reaction.message.edit(embed=embed)
            return
        elif author_field.split(' ')[-1] == 'Tracks':
            embed = _embed_tt(username, period, new_page)
            await reaction.message.edit(embed=embed)
            return
        elif author_field.split(' ')[-1] == 'Albums':
            embed = _embed_talb(username, period, new_page)
            await reaction.message.edit(embed=embed)
            return


async def _add_lf_emojis(message):
    await message.add_reaction('⬅')
    await message.add_reaction('➡')
    await message.add_reaction('❌')


def _lf_period(argument):
    if argument in ['7-days', 'week']:
        period = '7day'
    elif argument in ['1-month', 'month']:
        period = '1month'
    elif argument in ['3-month', 'quarter']:
        period = '3month'
    elif argument in ['6-month', 'half-year']:
        period = '6month'
    elif argument in ['12-month','year']:
        period = '12month'
    elif argument in ['alltime']:
        period = 'overall'
    else:
        period = 'overall'
    return period


def _embed_ta(username, period, page):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={LF_API_KEY}&period={period}&limit=10&page={page}&format=json')
    data = json.loads(response.text)
    response_user = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LF_API_KEY}&format=json')
    data_user = json.loads(response_user.text)

    content = ''
    for artist in data['topartists']['artist']:
        content += f"`{artist['@attr']['rank']}` [{artist['name']}]({quote(artist['url']).replace('%3A',':')}) ({artist['playcount']} plays)\n"

    embed = discord.Embed(
        title='', 
        colour=discord.Colour(0xD92323), 
        url='', 
        description=content, 
        timestamp=datetime.utcnow()
        )

    embed.set_thumbnail(url=data['topartists']['artist'][0]['image'][-1]['#text'])
    embed.set_author(name=f"{username}'s {period} Top Artists", url=f"https://www.last.fm/user/{username}", icon_url=data_user['user']['image'][0]['#text'])
    embed.set_footer(text=f"Page {page}/{data['topartists']['@attr']['totalPages']} | Last.fm | Total Scrobbles {data_user['user']['playcount']}", 
                    icon_url="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_lastfm-512.png")

    return embed


def _embed_tt(username, period, page):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={username}&api_key={LF_API_KEY}&period={period}&limit=10&page={page}&format=json')
    data = json.loads(response.text)
    response_user = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LF_API_KEY}&format=json')
    data_user = json.loads(response_user.text)

    content = ''
    for track in data['toptracks']['track']:
        content += f"`{track['@attr']['rank']}` [{track['name']}]({quote(track['url']).replace('%3A',':')}) "
        content += f"by [{track['artist']['name']}]({quote(track['artist']['url']).replace('%3A',':')}) "
        content += f"({track['playcount']} plays)\n"

    embed = discord.Embed(
        title='', 
        colour=discord.Colour(0xD92323), 
        url='', 
        description=content, 
        timestamp=datetime.utcnow()
        )

    embed.set_thumbnail(url=data['toptracks']['track'][0]['image'][-1]['#text'])
    embed.set_author(name=f"{username}'s {period} Top Tracks", url=f"https://www.last.fm/user/{username}", icon_url=data_user['user']['image'][0]['#text'])
    embed.set_footer(text=f"Page {page}/{data['toptracks']['@attr']['totalPages']} | Last.fm | Total Scrobbles {data_user['user']['playcount']}", 
                    icon_url="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_lastfm-512.png")

    return embed


def _embed_talb(username, period, page):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={username}&api_key={LF_API_KEY}&period={period}&limit=10&page={page}&format=json')
    data = json.loads(response.text)
    response_user = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LF_API_KEY}&format=json')
    data_user = json.loads(response_user.text)

    content = ''
    for album in data['topalbums']['album']:
        content += f"`{album['@attr']['rank']}` [{album['name']}]({quote(album['url']).replace('%3A',':')}) "
        content += f"by [{album['artist']['name']}]({quote(album['artist']['url']).replace('%3A',':')}) "
        content += f"({album['playcount']} plays)\n"

    embed = discord.Embed(
        title='', 
        colour=discord.Colour(0xD92323), 
        url='', 
        description=content, 
        timestamp=datetime.utcnow()
        )

    embed.set_thumbnail(url=data['topalbums']['album'][0]['image'][-1]['#text'])
    embed.set_author(name=f"{username}'s {period} Top Albums", url=f"https://www.last.fm/user/{username}", icon_url=data_user['user']['image'][0]['#text'])
    embed.set_footer(text=f"Page {page}/{data['topalbums']['@attr']['totalPages']} | Last.fm | Total Scrobbles {data_user['user']['playcount']}", 
                    icon_url="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_lastfm-512.png")

    return embed


def _embed_recent(username, page):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LF_API_KEY}&limit=10&page={page}&format=json')
    data = json.loads(response.text)
    response_user = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LF_API_KEY}&format=json')
    data_user = json.loads(response_user.text)

    content = ''
    time_now = datetime.utcnow()
    for track in data['recenttracks']['track']:
        if '@attr' in track.keys() and page != 1:
            continue

        content += '`*` '
        content += f"[{track['name']} by {track['artist']['#text']} ]({quote(track['url']).replace('%3A',':')}) "

        if '@attr' in track.keys():
            content += "- *Now Playing*\n"
        else:
            time_track = datetime.utcfromtimestamp(int(track['date']['uts']))
            time_diff = time_now - time_track

            if time_diff.days > 0:
                if time_diff.days > 1:
                    plural_suffix = 's'
                else:
                    plural_suffix = ''
                content += f"- {time_diff.days} day{plural_suffix} ago\n"
                continue
            if time_diff.seconds/3600 >= 1:
                if int(time_diff.seconds/3600) > 1:
                    plural_suffix = 's'
                else:
                    plural_suffix = ''
                content += f"- {int(time_diff.seconds/3600)} hour{plural_suffix} ago\n"
                continue
            if time_diff.seconds/60 >= 1:
                if int(time_diff.seconds/60) > 1:
                    plural_suffix = 's'
                else:
                    plural_suffix = ''
                content += f"- {int(time_diff.seconds/60)} minute{plural_suffix} ago\n"
                continue
            if time_diff.seconds > 0:
                if time_diff.seconds > 1:
                    plural_suffix = 's'
                else:
                    plural_suffix = ''
                content += f"- {time_diff.seconds} second{plural_suffix} ago\n"
                continue

    embed = discord.Embed(
        title='', 
        colour=discord.Colour(0xD92323), 
        url='', 
        description=content, 
        timestamp=time_now
        )

    embed.set_thumbnail(url=data['recenttracks']['track'][0]['image'][-1]['#text'])
    embed.set_author(name=f"{username}'s Recent Tracks", url=f"https://www.last.fm/user/{username}", icon_url=data_user['user']['image'][0]['#text'])
    embed.set_footer(text=f"Page {page}/{data['recenttracks']['@attr']['totalPages']} | Last.fm | Total Scrobbles {data_user['user']['playcount']}", 
                    icon_url="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_lastfm-512.png")

    return embed


def _embed_np(username):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LF_API_KEY}&limit=2&page=1&format=json')
    data = json.loads(response.text)
    response_user = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LF_API_KEY}&format=json')
    data_user = json.loads(response_user.text)

    if '@attr' in data['recenttracks']['track'][0].keys():
        title = f"{username} is currently listening to"
        content = ':notes: '
    else:
        title = f"{username} last listened to"
        content = ''

    for key, track in enumerate(data['recenttracks']['track'][:2]):
        if key == 0:
            content += f"[{track['name']} by {track['artist']['#text']}]({quote(track['url']).replace('%3A',':')})\n"
            content += f"**Album**\n"
            content += f"{track['album']['#text']}\n\n"
        else:
            content += f"**Listened to before**\n"
            content += f"[{track['name']} by {track['artist']['#text']}]({quote(track['url']).replace('%3A',':')})"

    embed = discord.Embed(
        title='', 
        colour=discord.Colour(0xD92323), 
        url='', 
        description=content, 
        timestamp=datetime.utcnow()
        )

    embed.set_author(name=title, url=f"https://www.last.fm/user/{username}", icon_url=data_user['user']['image'][0]['#text'])
    embed.set_thumbnail(url=data['recenttracks']['track'][0]['image'][-1]['#text'])
    embed.set_footer(text=f"Last.fm | Total Scrobbles {data_user['user']['playcount']}", 
                    icon_url="https://cdn2.iconfinder.com/data/icons/social-icon-3/512/social_style_3_lastfm-512.png")


    return embed
