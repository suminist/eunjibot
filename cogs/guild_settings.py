import discord
from discord.ext import commands
from models.guild_settings import AllGuildSettingsModel

settings = AllGuildSettingsModel()

class GuildSettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setprefix(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Please enter the new prefix.')
            return
    
        new_prefix = args[0]
        guild_id = ctx.guild.id
        settings.set_guild_settings(id=guild_id, prefix=new_prefix)

        await ctx.send(f'Prefix for this server is set to {new_prefix}')

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.guild.id
        prefix = settings.get_guild_settings(str(guild_id))['prefix']

        if message.content.startswith(prefix):
            message.content = message.content.replace(prefix, '~', 1)
            await self.bot.process_commands(message)