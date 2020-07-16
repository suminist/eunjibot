from datetime import datetime
import discord
from discord.ext import commands, tasks
from secret_keys import MONGODB_CONNECTION

import pymongo
myclient = pymongo.MongoClient(MONGODB_CONNECTION)
feeds_tt = myclient.overall.feeds_tt

from TikTokApi import TikTokApi
api = TikTokApi()

class TiktokCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._index = 0
        self._tiktok_scraper.start()

    @commands.command(aliases=['tt'])
    async def tiktok(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Wrong arguments.')
            return

        if args[0] in ['add']:
            await self._add_feed(ctx, args[1:])
        elif args[0] in ['delete']:
            await self._delete_feed(ctx, args[1:])
        elif args[0] in ['list']:
            await self._list_feeds(ctx)
        else:
            await ctx.send('Wrong arguments.')

    async def _add_feed(self, ctx, args):
        if len(args) != 2:
            await ctx.send('Invalid arguments. Please do `tiktok add <username> <text channel>`')
            return

        try:
            channel = await commands.TextChannelConverter().convert(ctx, args[1])
        except:
            await ctx.send('Invalid text channel.')
            return

        try:
            user = api.getUser(args[0])
            if user['statusCode'] != 0:
                raise Exception('invalid username')
        except Exception as e:
            print(e)
            await ctx.send('Invalid TikTok username.')
            return

        if _db_add_feed(user, channel.id) == False:
            await ctx.send('Already existing.')
            return

        await ctx.send(f'{ctx.guild.me.mention} will now update new posts of `{user.username}` to {channel.mention}.')
        
    async def _delete_feed(self, ctx, args):
        if len(args) == 0:
            await ctx.send('Please include the feed numbers to delete `tiktok delete <feed number> <feed number> ...`\nYou can use `tiktok list` to list the feeds.')
            return

        users = _db_get_tt_users()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id) for x in range(0,len(guild_channels))]

        response = f'Stopped following:\n'

        feed_counter = 0
        for user in users:
            for feed_channel_id in user['channels']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1
                    if str(feed_counter) in args:
                        channel = guild_channels[guild_channels_ids.index(feed_channel_id)]
                        _db_delete_feed(user['_id'], channel.id)
                        response = response + f'`{feed_counter}` Stopped following `{user["username"]}` in {channel.mention}\n'

        await ctx.send(response)

    async def _list_feeds(self, ctx):
        users = _db_get_tt_users()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id) for x in range(0,len(guild_channels))]

        response = f'Followed accounts for `{ctx.guild.name}`:\n'

        feed_counter = 0
        for user in users:
            for feed_channel_id in user['channels']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1
                    channel = guild_channels[guild_channels_ids.index(feed_channel_id)]
                    response = response + f'`{feed_counter}` Following `{user["username"]}` in {channel.mention}\n'

        await ctx.send(response)

    @tasks.loop(hours=40)
    async def _tiktok_scraper(self):
        if self.bot.is_ready() == False:
            return

        print("TT task: Starting")

        try:
            tt_users = _db_get_tt_users()
            if self._index >= feeds_tt.count():
                self._index = 0
            
            for tt_user in tt_users[self._index:self._index+1]:
                try:
                    tiktoks = api.byUsername(tt_user['username'], count=5)
                    latest_post_time = tt_user['latest_post_time']
                except Exception as e:
                    print(e)
                    return

                for tiktok in reversed(tiktoks):
                    if int(latest_post_time) >= int(tiktok['createTime']):
                        continue

                    for channel_id in tt_user['channels']:
                        try:
                            channel = await self.bot.fetch_channel(channel_id)
                            await channel.send(f"https://www.tiktok.com/@{tt_user['username']}/video/{tiktok['id']}")
                        except:
                            print(f'Cannot post in channel {channel_id}')

                    _db_update_latest_post(user, medias[0].created_time)  
                  
                print(f"Done {user.username}")

            self._index += 1

        except Exception as e:
            print('TT task ERROR')
            print(e)

def _db_get_tt_users():
    return feeds_tt.find()

def _db_update_latest_post(user, time):
    myquery = { "_id": str(user['userInfo']['user']['id']) }
    newvalues = { "$set": { "latest_post_time": time } }
    feeds_tt.update_one(myquery, newvalues)

def _db_add_feed(user, channel_id):
    myquery = { "_id": str(user['userInfo']['user']['id']) }
    user_document = feeds_tt.find_one(myquery)

    print(channel_id)
    print(user_document)
    if user_document == None:
        new_user_content = {
            '_id' : str(user['userInfo']['user']['id']),
            'username' : str(user.username),
            'latest_post_time' : int(datetime.now().timestamp()),
            'channels' : [str(channel_id)]
        }
        feeds_tt.insert_one(new_user_content)
        return

    channels_array = user_document['channels']

    if str(channel_id) in channels_array:
        return False

    channels_array.append(str(channel_id))
    print(channels_array)

    newvalues = { "$set": { "channels" : channels_array } }
    feeds_tt.update_one(myquery, newvalues)
    
    return

def _db_delete_feed(user_id, channel_id):
    myquery = { "_id": str(user_id) }
    user_document = feeds_tt.find_one(myquery)

    print(channel_id)
    print(user_document)
    if user_document == None:
        return

    channels_array = user_document['channels']

    channels_array.remove(str(channel_id))

    if len(channels_array) == 0:
        feeds_tt.delete_one(myquery)
        return
    
    newvalues = { "$set": { "channels" : channels_array } }
    feeds_tt.update_one(myquery, newvalues)
    
    return
