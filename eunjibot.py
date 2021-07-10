import discord
from discord.ext import commands, tasks

from cogs.management import ManagementCog
from cogs.lastfm import LastFmCog
from cogs.misc import MiscCog
from cogs.weather import WeatherCog
from cogs.guild_settings import GuildSettingsCog
from cogs.instagram import InstagramCog
from cogs.twitter import TwitterCog
from cogs.info import InfoCog
from cogs.welcome import WelcomeCog

from secret_keys import DISCORD_BOT_TOKEN

intents = discord.Intents.all()

async def blank(*args):
    pass

client = commands.Bot(command_prefix = '~', activity = discord.Game("Siwoo Cute"), case_insensitive=True, intents=intents)
client.on_message = blank

client.remove_command('help')
client.add_cog(ManagementCog(client))
client.add_cog(LastFmCog(client))
client.add_cog(MiscCog(client))
client.add_cog(WeatherCog(client))
client.add_cog(InfoCog(client))
client.add_cog(WelcomeCog(client))
client.add_cog(TwitterCog(client))
#client.add_cog(InstagramCog(client))

client.add_cog(GuildSettingsCog(client))

@client.before_invoke
async def before_any_command(ctx):
    try:
        await ctx.trigger_typing()
    except:
        pass

client.run(DISCORD_BOT_TOKEN)
