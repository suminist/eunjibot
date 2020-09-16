import discord
from discord.ext import commands
from db import guilds


class GuildSettingsCog(commands.Cog):
    """
    For guild settings.
    """
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "GuildSettings"

    @commands.command(
        description="Set prefix for this server",
        usage="Args:\n" +
              "- Prefix"
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def setprefix(self, ctx, *args):
        if len(args) == 0:
            await ctx.send('Please enter the new prefix.')
            return

        new_prefix = args[0]
        guild_id = ctx.guild.id
        await guilds.db_set_prefix(guild_id, prefix=new_prefix)

        await ctx.send(f'Prefix for this server is set to {new_prefix}')

    @commands.command(
        description="Set the modrole for this server. This will allow members with role to do some commands, like twitter and welcome commands.",
        usage="Args:\n" +
              "- Role"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def modrole(self, ctx, *args):
        if len(args) == 0:
            try:
                moderator_role_id = await guilds.db_get_moderator_role_id(ctx.guild.id)
                moderator_role = await commands.RoleConverter().convert(ctx, moderator_role_id)
                await ctx.send(f"The current moderator role is {moderator_role.mention}")
            except Exception as e:
                await ctx.send("There is no moderator role")

            return

        try:
            moderator_role = await commands.RoleConverter().convert(ctx, args[0])
        except Exception as e:
            print(e)
            await ctx.send("Invalid role")
            return

        await guilds.db_set_moderator_role_id(ctx.guild.id, moderator_role.id)
        await ctx.send(f"{moderator_role.mention} set as moderator role for this server.")

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.guild.id

        prefix = await guilds.db_get_prefix(guild_id)

        if prefix is None:
            prefix = '~'

        if message.content.startswith(prefix):
            message.content = message.content.replace(prefix, '~', 1)
            await self.bot.process_commands(message)
