import discord
from discord.ext import commands


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def botinfo(self, ctx):
        response_text = "This bot is in the following servers:\n"
        for guild in self.bot.guilds:
            response_text += f"`-` {guild.name}\n"

        await ctx.send(response_text)