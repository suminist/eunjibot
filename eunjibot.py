import discord
from discord.ext import commands, tasks

from cogs.management import Management
from cogs.lastfm import LastFM
from cogs.misc import Misc
from cogs.weather import Weather

from secret_keys import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix = '~', activity = discord.Game("Eunji bot under development"))

client.add_cog(Management(client))
client.add_cog(LastFM(client))
client.add_cog(Misc(client))
client.add_cog(Weather(client))

client.run(DISCORD_BOT_TOKEN)