import discord
from discord.ext import commands
import requests
import pylast
from secret_keys import LF_API_KEY, LF_API_SECRET, MONGODB_CONNECTION

import pymongo
myclient = pymongo.MongoClient(MONGODB_CONNECTION)
users = myclient.users.info

network = pylast.LastFMNetwork(api_key=LF_API_KEY, api_secret=LF_API_SECRET)

class LastFM(commands.core.Command):
    def __init__(self):
        commands.core.Command.__init__(self, self.function)
        self.name = 'lastfm'
        self.aliases = ['lf']

    async def function(self, ctx, *args):
        if len(args) == 0:
            await self._now_playing(ctx, args[1:])
        elif args[0] in ['ta', 'topartists']:
            await self._top_artists(ctx, args[1:])
        elif args[0] in ['set']:
            await self._set_username(ctx, args[1:])
        elif args[0] in ['np', 'nowplaying']:
            await self._now_playing(ctx, args[1:])          

    async def _top_artists(self, ctx, args):
        author_id = ctx.message.author.id
        username = self._db_get_username(author_id)

        if username == None:
            await ctx.send('Please register your username with `lf set username`')
            return
        
        if len(args) > 0:
            if args[0] in ['7-days', 'week']:
                period = '7day'
            elif args[0] in ['1-month', 'month']:
                period = '1month'
            elif args[0] in ['3-month', 'quarter']:
                period = '3month'
            elif args[0] in ['6-month', 'half-year']:
                period = '6month'
            elif args[0] in ['12-month','year']:
                period = '12month'
            elif args[0] in ['alltime']:
                period = 'overall'
            else:
                period = 'overall'
        else:
            period = 'overall'

        if period == '7day':
            title = f'Weekly top artists for {username}'
        elif period == '1month':
            title = f'Monthly top artists for {username}'
        elif period == '3month':
            title = f'Quarterly top artists for {username}'
        elif period == '6month':
            title = f'Half-yearly top artists for {username}'
        elif period == '12month':
            title = f'Yearly top artists for {username}'
        elif period == 'overall':
            title = f'All time top artists for {username}'

        embed = discord.Embed(
            title = title,
            color = 0x65E1F0
        )

        artists = network.get_user(username).get_top_artists(period=period, limit=10)

        for artist in artists:
            embed.add_field(name=artist.item, value=artist.weight, inline=False)

        await ctx.send(embed=embed)

    async def _now_playing(self, ctx, args):
        author_id = ctx.message.author.id
        username = self._db_get_username(author_id)

        if username == None:
            await ctx.send('Please register your username with `lf set username`')
            return

        embed = discord.Embed(
            title = '',
            color = 0x65E1F0
        )
        output = network.get_user(username).get_now_playing()
        embed.add_field(name='Now Playing', value=output, inline=False)
        await ctx.send(embed=embed)

    async def _set_username(self, ctx, args):
        if len(args) == 0:
            await ctx.send('Please include username `lf set username`')
            return

        author_id = ctx.message.author.id
        username = args[0]

        self._db_set_username(author_id, username)
        await ctx.send(f"Set username to {username}")

    def _db_set_username(self, id, username):
        user = users.find_one({"id": f"{id}"})

        if user == None:
            newvalues = { "id" : f"{id}", "lfUsername": username}
            users.insert_one(newvalues)
        else:
            myquery = { "id": f"{id}" }
            newvalues = { "$set": { "lfUsername": username } }
            users.update_one(myquery, newvalues)

    def _db_get_username(self, id):
        try:
            username = users.find_one({"id": f"{id}"})['lfUsername']
            return username
        except Exception as e:
            print(e)
            return None
