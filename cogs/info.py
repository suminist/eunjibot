import discord
from discord.ext import commands
from db import guilds


class InfoCog(commands.Cog):
    """
    Information stuff kek
    """
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Information"

    @commands.command(
        description="Show information about the bot.",
        usage="Args: None"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def botinfo(self, ctx):
        response_text = f"This bot is in {len(self.bot.guilds)} servers:"
        for guild in self.bot.guilds:
            response_text += f"`-` {guild.name}\n"

        await ctx.send(response_text)

    @commands.command(
        description="Show help messages for the bot commands",
        usage="Args:\n" +
              "- category name (optional)"
    )
    @commands.guild_only()
    async def help(self, ctx, cog_name=None):
        prefix = await guilds.db_get_prefix(ctx.guild.id)
        
        cogs = {k.lower(): v for k, v in self.bot.cogs.items()}

        if cog_name and cog_name.lower() in cogs.keys():
            cog = cogs[cog_name.lower()]
            description = "**Here are the commands you can run:**\n\n"

            for command in cog.walk_commands():
                if not isinstance(command, commands.Group):

                    if command.root_parent is None or await command.root_parent.can_run(ctx):
                        description += f"`{prefix}{command.qualified_name}`:\n"

                        if command.description !=  "":
                            description += f"{command.description}\n"
                        else:
                            description += "No description\n"

                        if command.usage is not None:
                            description += f"{command.usage}\n"

                        description += "\n"

            embed = discord.Embed(color=0xFE7DFA, title=f"{cog.qualified_name}", description=description)
            await ctx.send(embed=embed)

        else:
            description = ""

            for cog in self.bot.cogs.values():
                description += f"**{cog.qualified_name}**: {cog.description}\n"

            description += f"\n\nGet more information by using `{prefix}help <category>`"
            embed = discord.Embed(color=0xFE7DFA, title="Bot Command Categories", description=description)

            if cog_name:
                await ctx.send(content=f"`{cog_name}` category not found.", embed=embed)
            else:
                await ctx.send(embed=embed)
