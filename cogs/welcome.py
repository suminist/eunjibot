import discord
from discord.ext import commands
from db import guilds


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def welcome(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Add more arguments')

    @welcome.command()
    async def channel(self, ctx, *args):
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

    @welcome.command()
    async def content(self, ctx):
        print(ctx.message.content)
        content = " ".join(ctx.message.content.split(" ")[2:])
        print(content)

        if content == "":
            await ctx.send("Please include the content")
            return

        await guilds.db_set_welcome_content(ctx.guild.id, content)
        embed = generateEmbed(
                ctx.author,
                await guilds.db_get_welcome_content(ctx.guild.id),
                await guilds.db_get_welcome_image_url(ctx.guild.id)
            )

        await ctx.send(embed=embed)

    @welcome.command()
    async def image(self, ctx, *args):
        image_url = " ".join(ctx.message.content.split(" ")[2:])

        if image_url == "":
            await ctx.send("Please include the image url")
            return

        await guilds.db_set_welcome_image_url(ctx.guild.id, image_url)
        embed = generateEmbed(
                ctx.author,
                await guilds.db_get_welcome_content(ctx.guild.id),
                await guilds.db_get_welcome_image_url(ctx.guild.id)
            )

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await guilds.db_set_welcome_image_url(ctx.guild.id, None)
            await ctx.send("Invalid image URL")

    @welcome.command()
    async def preview(self, ctx):
        embed = generateEmbed(
                ctx.author,
                await guilds.db_get_welcome_content(ctx.guild.id),
                await guilds.db_get_welcome_image_url(ctx.guild.id)
            )

        await ctx.send(
            f"Welcome channel in <#{await guilds.db_get_welcome_channel_id(ctx.guild.id)}>",
            embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = await guilds.db_get_welcome_channel_id(member.guild.id)

        if channel_id is None:
            return

        channel = member.guild.get_channel(channel_id)
        if channel is None:
            print(f"Cannot welcome {member} to {member.guild.name} (invalid channel)")
            return

        embed = generateEmbed(
                member,
                await guilds.db_get_welcome_content(member.guild.id),
                await guilds.db_get_welcome_image_url(member.guild.id)
            )

        await channel.send(embed=embed)


def generateEmbed(member, content, image_url):
    if content is None:
        content = "Welcome to {guild}, {member}"

    content = content.replace("{guild}", member.guild.name)
    content = content.replace("{member}", member.mention)

    embed = discord.Embed(color=0xFE7DFA, title='New Member Join', description=content)
    embed.set_thumbnail(url=member.avatar_url)
    if image_url is not None:
        embed.set_image(url=image_url)
    embed.set_footer(text=f"Member #{len(member.guild.members)}")

    return embed
