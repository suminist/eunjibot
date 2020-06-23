import discord
from discord.ext import commands

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, *args):
        if ctx.author.guild_permissions.ban_members == False:
            await ctx.send('You have no permissions to ban members.')
            return
        
        if ctx.guild.me.guild_permissions.ban_members == False:
            await ctx.send('The bot has no permissions to ban members.')
            return

        if len(args) == 0:
            await ctx.send('Please enter the user to ban.')
            return

        try:
            member_to_ban = await commands.MemberConverter().convert(ctx, args[0])
        except Exception as e:
            await ctx.send(e)
            return
        
        if member_to_ban.top_role.position >= ctx.author.top_role.position:
            await ctx.send('You cannot ban a member who is not lower than you.')
            return

        try:
            await member_to_ban.ban(reason='Test')
            await ctx.send(f'User {member_to_ban.display_name} has been banned.')
            return
        except Exception as e:
            await ctx.send(e)
            return


    @commands.command()
    async def kick(self, ctx, *args):
        if ctx.author.guild_permissions.kick_members == False:
            await ctx.send('You have no permissions to kick members.')
            return
        
        if ctx.guild.me.guild_permissions.kick_members == False:
            await ctx.send('The bot has no permissions to kick members.')
            return

        if len(args) == 0:
            await ctx.send('Please enter the user to kick.')
            return

        try:
            member_to_kick = await commands.MemberConverter().convert(ctx, args[0])
        except Exception as e:
            await ctx.send(e)
            return
        
        if member_to_kick.top_role.position >= ctx.author.top_role.position:
            await ctx.send('You cannot kick a member who is not lower than you.')
            return

        try:
            await member_to_kick.kick(reason='Test')
            await ctx.send(f'User {member_to_kick.display_name} has been kicked.')
        except Exception as e:
            await ctx.send(e)
            return

    
    @commands.command()
    async def mute(self, ctx, *args):
        if ctx.author.guild_permissions.manage_roles == False:
            await ctx.send('You have no permissions to manage roles.')
            return
        
        if ctx.guild.me.guild_permissions.manage_roles == False:
            await ctx.send('The bot has no permissions to manage roles.')
            return

        if len(args) == 0:
            await ctx.send('Please enter the user to mute.')
            return

        try:
            member_to_mute = await commands.MemberConverter().convert(ctx, args[0])
        except Exception as e:
            await ctx.send(e)
            return

        if member_to_mute.top_role.position >= ctx.author.top_role.position:
            await ctx.send('You cannot mute a member who is not lower than you.')
            return

        mute_role = None
        for role in ctx.guild.roles:
            if role.name.lower() == 'mute':
                mute_role = role
                break

        if mute_role == None:
            try:
                mute_role = await ctx.guild.create_role(name='mute')
                for channel in ctx.guild.channels:
                    try:
                        await channel.set_permissions(mute_role, send_messages=False, speak=False, add_reactions=False)   
                        print(f'Successfully overwritten permissions on channel {channel.name}')
                    except Exception as e:
                        print(f'Failed to overwrite permissions on channel {channel.name}')  
                        print(e)
                        
            except Exception as e:
                await ctx.send(e)
                return

        try:
            await member_to_mute.add_roles(mute_role)
            await ctx.send(f'User {member_to_mute.display_name} has been muted.')

        except Exception as e:
            await ctx.send(e)
            return
