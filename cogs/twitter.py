from discord.ext import commands, tasks
from db import feeds_twitter, guilds
import tweepy
import traceback
import shlex

from threading import Thread
from queue import Queue
from asyncio import Event, sleep

from secret_keys import TWT_CONSUMER_KEY, TWT_CONSUMER_SECRET, TWT_ACCESS_TOKEN, TWT_ACCESS_TOKEN_SECRET


class TwitterCog(commands.Cog):
    """
    Follow twitter feeds
    """

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Twitter"
        self.to_update_stream = False
        self.api = None
        self.key_set = 1
        self.feeds_list = []
        self.stream = None
        self.tweet_queue = Queue()
        self.tweet_event = Event()
        self.initialize.start()
        self.tweet_handler.start()

    @tasks.loop(count=1)
    async def initialize(self):
        try:
            await self.update_feeds()
            self.restart_stream()

        except Exception:
            traceback.print_exc()

    @tasks.loop(seconds=0)
    async def tweet_handler(self):
        try:
            await self.tweet_event.wait()
            while self.tweet_queue.qsize() > 0:
                tweet = self.tweet_queue.get()

                for channel_id in tweet["channel_ids"]:
                    try:
                        channel = await self.bot.fetch_channel(channel_id)
                        await channel.send(tweet["url"])
                    except Exception:
                        print(f'Cannot post in channel {channel_id}')

            self.tweet_event.clear()

        except Exception:
            traceback.print_exc()

    async def moderator_role_check(ctx):
        if ctx.author.guild_permissions.administrator is True:
            return True

        try:
            moderator_role_id = await guilds.db_get_moderator_role_id(ctx.guild.id)
            moderator_role = await commands.RoleConverter().convert(ctx, moderator_role_id)
        except Exception as e:
            print(e)
            return False

        return ctx.author.top_role >= moderator_role

    @commands.group(case_insensitive=True)
    @commands.guild_only()
    @commands.check(moderator_role_check)
    async def twitter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.feeds)

    @twitter.command(
        description="Follow a user to a discord channel",
        usage="Args:\n" +
              "- Twitter username\n" +
              "- Text channel"
    )
    async def add(self, ctx, *, arg=""):
        args = shlex.split(arg)

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
            await ctx.send(
                f'{ctx.guild.me.mention} will now update new tweets of `{user.screen_name}` to {channel.mention}.'
            )

            self.to_update_stream = True

            await sleep(20)
            await self.update_feeds()

            if self.to_update_stream:
                self.restart_stream()

        elif result is False:
            await self.update_feeds()
            await ctx.send(
                f'{ctx.guild.me.mention} will now update new tweets of `{user.screen_name}` to {channel.mention}.'
            )

        else:
            await ctx.send('Already existing.')

    @twitter.command(
        description="Stop selected feeds. Get the index needed using `feeds`.\n" +
                    "For example `twitter delete 1 2 3 4` will delete feeds 1, 2, 3, and 4.",
        usage="Args:\n" +
              "- Feed index/es"
    )
    async def delete(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Please include the feed numbers to delete `twitter delete <feed number> <feed number> ...`\nYou can use `twitter feeds` to list the feeds.')
            return

        self.feeds_list[:] = await feeds_twitter.db_get_feeds()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id)
                              for x in range(0, len(guild_channels))]

        response = ""

        deleted_feed_counter = 0
        feed_counter = 0
        for feed in self.feeds_list:
            try:
                user = self.api.get_user(id=feed["_id"])
            except Exception:
                traceback.print_exc()
            for feed_channel_id in feed['channelIds']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1
                    if str(feed_counter) in args:
                        await feeds_twitter.db_delete_feed(user.id, feed_channel_id)
                        response = response + \
                            f'`{feed_counter}` Stopped following `{user.screen_name}` in <#{feed_channel_id}>\n'
                        deleted_feed_counter += 1

        if deleted_feed_counter == 0:
            response = "Deleted nothing. Make sure your feed numbers are correct.\n" +\
                "Use `twitter feeds` to see the feed numbers.\n" +\
                "Then use `twitter delete 1 5` to delete feeds 1, and 5, for example"
        else:
            response = 'Stopped following:\n' + response

        await ctx.send(response)
        await self.update_feeds()

    @twitter.command(
        description="List all the twitter feeds in this server",
        usage="Args: None"
    )
    async def feeds(self, ctx):
        self.feeds_list[:] = await feeds_twitter.db_get_feeds()
        guild_channels = ctx.guild.channels
        guild_channels_ids = [str(guild_channels[x].id)
                              for x in range(0, len(guild_channels))]

        response = f'Followed accounts for `{ctx.guild.name}`:\n'

        feed_counter = 0
        for feed in self.feeds_list:
            for feed_channel_id in feed['channelIds']:
                if feed_channel_id in guild_channels_ids:
                    feed_counter += 1

                    try:
                        user = self.api.get_user(id=feed["_id"])
                        response = response + \
                            f'`{feed_counter}` Following `{user.screen_name}` in <#{feed_channel_id}>\n'

                    except Exception:
                        traceback.print_exc()

        await ctx.send(response)

    async def update_feeds(self):
        self.feeds_list[:] = await feeds_twitter.db_get_feeds()

    def restart_stream(self):
        print("Updated stream")
        self.to_update_stream = False

        if self.key_set == 2:
            self.key_set = 0
        else:
            self.key_set += 1

        auth = tweepy.OAuthHandler(
            TWT_CONSUMER_KEY.split(" ")[self.key_set],
            TWT_CONSUMER_SECRET.split(" ")[self.key_set]
        )
        auth.set_access_token(
            TWT_ACCESS_TOKEN.split(" ")[self.key_set],
            TWT_ACCESS_TOKEN_SECRET.split(" ")[self.key_set]
        )
        self.api = tweepy.API(auth)

        if self.stream is not None:
            self.stream.disconnect()

        self.stream = MyStream(
            twitter_cog=self,
            auth=self.api.auth,
            listener=MyStreamListener(
                self.feeds_list, self.tweet_queue, self.tweet_event)
        )
        self.stream.filter(follow=[self.feeds_list[x]["_id"]
                           for x in range(0, len(self.feeds_list))], is_async=True)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, feeds_list, tweet_queue, tweet_event):
        super(MyStreamListener, self).__init__()
        self.feeds_list = feeds_list
        self.tweet_queue = tweet_queue
        self.tweet_event = tweet_event

    def on_status(self, status):
        try:
            if str(status.user.id) in [self.feeds_list[x]["_id"] for x in range(0, len(self.feeds_list))]:
                feed = list(filter(lambda feed: feed["_id"] == str(
                    status.user.id), self.feeds_list))[0]

                tweet_url = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
                channel_ids = feed["channelIds"]

                self.tweet_queue.put(
                    {"url": tweet_url, "channel_ids": channel_ids})
                self.tweet_event.set()

        except Exception:
            traceback.print_exc()

    def on_error(self, status):
        print(status)


class MyStream(tweepy.Stream):
    def __init__(self, twitter_cog, *args, **kwargs):
        super(MyStream, self).__init__(*args, **kwargs)
        self.twitter_cog = twitter_cog

    def _start(self, is_async):
        self.running = True
        if is_async:
            self._thread = Thread(target=self._run)
            self._thread.daemon = self.daemon
            self._thread.name = "twitter_streaming_thread"
            self._thread.start()
        else:
            self._run()

    def _run(self):
        try:
            super(MyStream, self)._run()
        except BaseException:
            print("Streaming thread crashed")
            self.twitter_cog.restart_stream()
