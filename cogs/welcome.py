import discord
from discord.ext import commands
from db import guilds


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def welcome(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please include channel")
            return

        try:
            channel = await commands.TextChannelConverter().convert(ctx, args[0])
        except Exception:
            await ctx.send('Invalid text channel.')
            return

        await guilds.db_set_welcome_channel_id(ctx.guild.id, channel.id)
        await ctx.send(f'Welcome channel is set to {channel.mention}.')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = await guilds.db_get_welcome_channel_id(member.guild.id)

        if channel_id is None:
            return

        channel = member.guild.get_channel(channel_id)
        if channel is None:
            print(f"Cannot welcome {member} to {member.guild.name} (invalid channel)")
            return

        await channel.send(f"Welcome to {member.guild.name}, {member.mention}!")
