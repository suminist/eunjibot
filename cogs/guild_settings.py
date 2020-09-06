import discord
from discord.ext import commands
from db import guilds


class GuildSettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def setprefix(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Please enter the new prefix.')
            return

        new_prefix = args[0]
        guild_id = ctx.guild.id
        await guilds.db_set_prefix(guild_id, prefix=new_prefix)

        await ctx.send(f'Prefix for this server is set to {new_prefix}')

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.guild.id

        prefix = await guilds.db_get_prefix(guild_id)

        if prefix is None:
            prefix = '~'

        if message.content.startswith(prefix):
            message.content = message.content.replace(prefix, '~', 1)
            await self.bot.process_commands(message)
