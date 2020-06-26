import discord
from discord.ext import commands, tasks

from cogs.management import ManagementCog
from cogs.lastfm import LastFmCog
from cogs.misc import MiscCog
from cogs.weather import WeatherCog
from cogs.guild_settings import GuildSettingsCog
from cogs.instagram import InstagramCog

from models.guild_settings import AllGuildSettingsModel
settings = AllGuildSettingsModel()

from secret_keys import DISCORD_BOT_TOKEN

async def blank(*args):
    pass

client = commands.Bot(command_prefix = '~', activity = discord.Game("Eunji bot under development"))
client.on_message = blank

client.add_cog(ManagementCog(client))
client.add_cog(LastFmCog(client))
client.add_cog(MiscCog(client))
client.add_cog(WeatherCog(client))
client.add_cog(InstagramCog(client))

client.add_cog(GuildSettingsCog(client))

client.run(DISCORD_BOT_TOKEN)
