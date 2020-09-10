import discord
from discord.ext import commands, tasks
from db import feeds_twitter
import tweepy
import traceback
import asyncio
from datetime import datetime, date, timedelta
import pytz

from secret_keys import TWT_CONSUMER_KEY, TWT_CONSUMER_SECRET, TWT_ACCESS_TOKEN, TWT_ACCESS_TOKEN_SECRET

# Set up OAuth and integrate with API


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, feeds, tweet_queue):
        super(MyStreamListener, self).__init__()
        self.feeds = feeds
        self.tweet_queue = tweet_queue

    def on_status(self, status):
        try:
            if str(status.user.id) in [self.feeds[x]["_id"] for x in range(0, len(self.feeds))]:
                feed = list(filter(lambda feed: feed["_id"] == str(status.user.id), self.feeds))[0]

                tweet_url = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
                channel_ids = feed["channelIds"]

                self.tweet_queue.append({"url": tweet_url, "channel_ids": channel_ids})
        except Exception:
            traceback.print_exc()

    def on_error(self, status):
        print(status)


class TwitterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.to_update_stream = False
        self.api = None
        self.key_set = 0
        self.feeds = []
        self.tweet_queue = []
        self.initialize.start()
        self.tweet_handler.start()

    @tasks.loop(count=1)
    async def initialize(self):
        try:
            auth = tweepy.OAuthHandler(TWT_CONSUMER_KEY.split(" ")[self.key_set], TWT_CONSUMER_SECRET.split(" ")[self.key_set])
            auth.set_access_token(TWT_ACCESS_TOKEN.split(" ")[self.key_set], TWT_ACCESS_TOKEN_SECRET.split(" ")[self.key_set])
            self.api = tweepy.API(auth)
            self.feeds[:] = await feeds_twitter.db_get_feeds()
            self.stream = tweepy.Stream(auth=self.api.auth, listener=MyStreamListener(self.feeds, self.tweet_queue))
            self.stream.filter(follow=[self.feeds[x]["_id"] for x in range(0, len(self.feeds))], is_async=True)
            print(self.feeds)
        except Exception:
            traceback.print_exc()

    @tasks.loop(seconds=1)
    async def tweet_handler(self):
        try:
            while len(self.tweet_queue) > 0:
                tweet = self.tweet_queue[0]

                for channel_id in tweet["channel_ids"]:
                    try:
                        channel = await self.bot.fetch_channel(channel_id)
                        await channel.send(tweet["url"])
                    except Exception:
                        print(f'Cannot post in channel {channel_id}')

                self.tweet_queue.remove(tweet)

        except Exception:
            traceback.print_exc()

    @commands.group(case_insensitive=True)
    @commands.guild_only()
    async def twitter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Add more arguments')

    @twitter.command()
    async def add(self, ctx, *args):
        if len(args) != 2:
            await ctx.send('Invalid arguments. Please do `twitter add <username> <text channel>`')
            return

        try:
            channel = await commands.TextChannelConverter().convert(ctx, args[1])
        except Exception:
            await ctx.send('Invalid text channel.')
            return

        try:
            user = self.api.get_user(screen_name=args[0])
        except Exception as e:
            print(e)
            await ctx.send(e)
            return

        result = await feeds_twitter.db_add_feed(user.id, channel.id)
        print(result)
        if result is True:
            await ctx.send(f'{ctx.guild.me.mention} will now update new tweets of `{user.screen_name}` to {channel.mention}.')

            self.to_update_stream = True
            self.feeds[:] = await feeds_twitter.db_get_feeds()

            await asyncio.sleep(20)

            if self.to_update_stream:
                print("UPDATED STREAM")
                self.to_update_stream = False

                if self.key_set == 2:
                    self.key_set = 0
                else:
                    self.key_set += 1

                auth = tweepy.OAuthHandler(TWT_CONSUMER_KEY.split(" ")[self.key_set], TWT_CONSUMER_SECRET.split(" ")[self.key_set])
                auth.set_access_token(TWT_ACCESS_TOKEN.split(" ")[self.key_set], TWT_ACCESS_TOKEN_SECRET.split(" ")[self.key_set])
                self.api = tweepy.API(auth)
                self.stream.disconnect()
                self.stream = tweepy.Stream(auth=self.api.auth, listener=MyStreamListener(self.feeds, self.tweet_queue))
                self.stream.filter(follow=[self.feeds[x]["_id"] for x in range(0, len(self.feeds))], is_async=True)
        elif result is False:
            self.feeds[:] = await feeds_twitter.db_get_feeds()
            await ctx.send(f'{ctx.guild.me.mention} will now update new tweets of `{user.screen_name}` to {channel.mention}.')
        else:
            await ctx.send('Already existing.')

    @twitter.command()
    async def delete(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Please include the feed numbers to delete `instagram delete <feed number> <feed number> ...`\nYou can use `instagram list` to list the feeds.')
            return

        self.feeds[:] = await feeds_twitter.db_get_feeds()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id) for x in range(0, len(guild_channels))]

        response = 'Stopped following:\n'

        feed_counter = 0
        for feed in self.feeds:
            try:
                user = self.api.get_user(id=feed["_id"])
            except Exception:
                traceback.print_exc()
            for feed_channel_id in feed['channelIds']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1
                    if str(feed_counter) in args:
                        await feeds_twitter.db_delete_feed(user.id, feed_channel_id)
                        response = response + f'`{feed_counter}` Stopped following `{user.screen_name}` in <#{feed_channel_id}>\n'

        await ctx.send(response)
        self.feeds[:] = await feeds_twitter.db_get_feeds()

    @twitter.command()
    async def feeds(self, ctx, *args):
        self.feeds[:] = await feeds_twitter.db_get_feeds()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id) for x in range(0, len(guild_channels))]

        response = f'Followed accounts for `{ctx.guild.name}`:\n'

        feed_counter = 0
        for feed in self.feeds:
            for feed_channel_id in feed['channelIds']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1
                    user = self.api.get_user(feed["_id"])
                    response = response + f'`{feed_counter}` Following `{user.screen_name}` in <#{feed_channel_id}>\n'

        await ctx.send(response)


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
