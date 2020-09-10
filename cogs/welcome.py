import discord
from discord.ext import commands
from db import guilds


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def moderator_role_check(ctx):
        if ctx.author.guild_permissions.administrator is True:
            return True

        try:
            moderator_role_id = await guilds.db_get_moderator_role_id(ctx.guild.id)
            moderator_role = await commands.RoleConverter().convert(ctx, moderator_role_id)
        except Exception as e:
            print(e)
            return False

        return ctx.author.top_role >= moderator_role

    @commands.group(case_insensitive=True)
    @commands.guild_only()
    @commands.check(moderator_role_check)
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

        await guilds.db_set_welcome(ctx.guild.id, welcome_channel_id=channel.id)
        await ctx.send(f'Welcome channel is set to {channel.mention}.')

    @welcome.command()
    async def title(self, ctx, *, title=""):
        if title == "":
            await ctx.send("Please include the title")
            return

        await guilds.db_set_welcome(ctx.guild.id, welcome_title=title)

        welcome_info = await guilds.db_get_welcome(ctx.guild.id)

        embed = generate_embed(
                ctx.author,
                welcome_info
            )

        await ctx.send(embed=embed)

    @welcome.command()
    async def content(self, ctx, *, content=""):
        if content == "":
            await ctx.send("Please include the content")
            return

        await guilds.db_set_welcome(ctx.guild.id, welcome_content=content)

        welcome_info = await guilds.db_get_welcome(ctx.guild.id)

        embed = generate_embed(
                ctx.author,
                welcome_info
            )

        await ctx.send(embed=embed)

    @welcome.command()
    async def image(self, ctx, *, image_url=""):
        if image_url == "":
            await ctx.send("Please include the image url")
            return

        await guilds.db_set_welcome(ctx.guild.id, welcome_image_url=image_url)

        welcome_info = await guilds.db_get_welcome(ctx.guild.id)

        embed = generate_embed(
                ctx.author,
                welcome_info
            )

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await guilds.db_set_welcome(ctx.guild.id, welcome_image_url="None")
            await ctx.send("Invalid image URL")

    @welcome.command()
    async def preview(self, ctx):
        welcome_info = await guilds.db_get_welcome(ctx.guild.id)

        embed = generate_embed(
                ctx.author,
                welcome_info
            )

        await ctx.send(
            f"Welcome channel in <#{welcome_info['channel_id']}>",
            embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_info = await guilds.db_get_welcome(member.guild.id)

        if welcome_info["channel_id"] is None:
            return

        channel = member.guild.get_channel(welcome_info["channel_id"])
        if channel is None:
            print(f"Cannot welcome {member} to {member.guild.name} (invalid channel)")
            return

        embed = generate_embed(
                member,
                welcome_info
            )

        await channel.send(embed=embed)


def generate_embed(member, welcome_info):
    title = welcome_info["title"]
    content = welcome_info["content"]
    image_url = welcome_info["image_url"]

    if title is None:
        title = "New Member Join"
    if content is None:
        content = "Welcome to {guild}, {member}"

    title = title.replace("{guild}", member.guild.name)
    title = title.replace("{member}", member.mention)
    content = content.replace("{guild}", member.guild.name)
    content = content.replace("{member}", member.mention)

    embed = discord.Embed(color=0xFE7DFA, title=title, description=content)
    embed.set_thumbnail(url=member.avatar_url)
    if image_url is not None:
        embed.set_image(url=image_url)
    embed.set_footer(text=f"Member #{len(member.guild.members)}")

    return embed
