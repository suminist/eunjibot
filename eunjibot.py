import discord
from discord.ext import commands, tasks

from cogs.management import ManagementCog
from cogs.lastfm import LastFmCog
from cogs.misc import MiscCog
from cogs.weather import WeatherCog

from secret_keys import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix = '~', activity = discord.Game("Eunji bot under development"))

client.add_cog(ManagementCog(client))
client.add_cog(LastFmCog(client))
client.add_cog(MiscCog(client))
client.add_cog(WeatherCog(client))

client.run(DISCORD_BOT_TOKEN)