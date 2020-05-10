import discord
from discord.ext import commands, tasks
import os
import random
from itertools import cycle
import json
from bs4 import BeautifulSoup as bSoup
import requests

token = 'NzA3NDU1NDAyNzQ0MjE3NjEw.XrcuXg.DpJ3zCZ6yD-6BAQURvps1YPM8EM'
gToken = 'abc'
client = commands.Bot(command_prefix = '~')

#bot m
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('running 24/7'))
    print('<<<<<=====<>=====<>=====Eunjibot Online=====<>=====<>=====>>>>>')

# @client.command()
# async def load(ctx, extension):
#     client.load_extension(f'cogs.{extension}')

# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'cogs.{extension}')

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         client.load_extension(f'cogs.{filename[:-3]}')

@client.command(aliases=['memes'])
async def _memes(ctx):
    responses = [
        'https://i.imgur.com/JncHCj9.jpg', #weird insta meme
        'https://imgur.com/FCNVmW6', #maggie's face
        'https://imgur.com/p4pw1tg', #pumpkin
        'https://imgur.com/iMJcc3A', #black maggie
        'https://imgur.com/CxgwHYN', #dabb maggie
        'https://imgur.com/Bt35YW0', #baby yoda
        'https://imgur.com/OENkvsx', #worms
        'https://imgur.com/adRS9G5', #trump
        'https://imgur.com/aPdT94e', #feelsweirdmansnapchat
        'https://imgur.com/Y2jv5OZ', #oddguy
        'https://imgur.com/3qOIIsm', #nancy
        'https://imgur.com/lytOnrm', #nancystare
        'https://imgur.com/uWXBfAS', #monies
        'https://imgur.com/rSCAiTy', #bigbois
    ]
    await ctx.send(random.choice(responses))

@client.command(aliases=['iconic'])
async def _iconic(ctx):
    responses = [
        'https://imgur.com/3DTXTQX',
        'https://cdn.discordapp.com/attachments/700882681545883650/707027412311081080/image2.jpg',
        'https://cdn.discordapp.com/attachments/700882681545883650/707027411937787955/image1.jpg',
    ]
    await ctx.send(random.choice(responses))

@client.command(aliases=['maggie'])
async def _maggie(ctx):
    responses = [
        'https://imgur.com/FCNVmW6', #maggie's face
        'https://imgur.com/iMJcc3A', #black maggie
        'https://imgur.com/CxgwHYN', #dabb maggie
        'https://imgur.com/OENkvsx', #worms
        'https://imgur.com/uWXBfAS', #monies
        'https://cdn.discordapp.com/attachments/707280448858095716/707468264178974771/image0-9.png' #snow
    ]
    await ctx.send(random.choice(responses))

#formatting for Emoji - Member Ping - Role Ping
# <:emote_name:emote_ID>
# <@!user_ID>
# <@&role_ID>

@client.command(aliases=['goodnight'])
async def _goodnight(ctx):
    iuwu = [
        'https://tenor.com/view/iu-cute-hug-sleeping-gif-15049574',
        'https://tenor.com/view/iu-sleep-sleepy-sleeping-tired-gif-12177560'
    ]
    await ctx.send(random.choice(iuwu))

@client.command(aliases=['emb1'])
async def _emb1(ctx):
    embed = discord.Embed(
        title = 'Jeong Eunji',
        description = 'Best Singer',
        color = 0xFF86E4
    )
    embed.set_author(name='Apink', icon_url='https://i.pinimg.com/originals/4b/4b/b7/4b4bb7a19133e996ff913e62ae43ca9f.jpg')
    embed.set_footer(text='Copyright JamJam 2020', icon_url='')
    embed.set_image(url='http://images6.fanpop.com/image/photos/39900000/-Jung-Eun-Ji-jung-eunji-39944017-540-810.jpg')
    embed.set_thumbnail(url='https://images-na.ssl-images-amazon.com/images/I/41laNGJDa3L.jpg')
    await ctx.send(embed=embed)

@client.command(aliases=['form1'])
async def _form1(ctx):
    embed = discord.Embed(
        title = 'Bitch Form',
        description = 'Fill this out if you or someone else is feeling bitchy',
        color = 0xEAFB19
    )
    file = discord.File('./forms/0form1.jpg')
    embed.set_image(url='attachment://0form1.jpg')
    await ctx.send(file=file, embed=embed)

# @tasks.loop(seconds=10)
# async def change_status():
#     status = cycle(['Playing with JamJam', 'Sleepy Time'])
#     await client.change_presence(activity=discord.Game(next(status)))

@client.command(aliases=['whatslunch'])
async def _whatslunch(ctx):
    lunch = [
        'Pasta',
        'Takeout',
        "Don't eat, have a snack instead",
        'Some fruits',
        'Mcdonalds'
    ]

    await ctx.send(random.choice(lunch))

@client.command(aliases=['ban'])
async def _ban(ctx):
    await ctx.send('Please add a user ID in order to execute the command')

@client.command(aliases=['latestcb'])
async def _latestcb(ctx):
    embed_IU = discord.Embed(
        title = 'IU - Lee Ji-Eun (이지은)',
        color = 0x4DFF29
    )

    embed_IU.set_thumbnail(url='https://i.imgur.com/M9p3WgK.jpg')
    embed_IU.set_image(url='https://channel-korea.com/wp-content/uploads/2017/09/IU_1476317492_af_org-e1506689157858.jpg')
    embed_IU.add_field(name='Member Profile', value='https://kprofiles.com/iu-profile/', inline=False)

    embed_IU.add_field(name='Latest Comeback',value='https://www.youtube.com/watch?v=TgOu00Mf3kI', inline=False)

    await ctx.send(embed=embed_IU)

@client.command(aliases=['apink'])
async def _apink(ctx, *, msg):

    members= ['eunji', 'bomi', 'hayoung', 'naeun', 'namjoo', 'chorong']

    for mem in members:
        if str(msg.lower()) == mem:
            link = f'https://kprofiles.com/{msg}-profile-facts/'
            emb_title = 'Member Profile'

            source = requests.get(link).text
            soup = bSoup(source, 'lxml')

            kp_f = soup.find('div', class_='entry-content').p.text #print these facts

            kp_jpg = soup.find('div', class_='entry-content').img
            kp_src = kp_jpg['src'] #print this image

            embed_kp = discord.Embed(
                title = emb_title,
                color = 0x29FFCE
            )

            embed_kp.add_field(name='Info', value=kp_f)
            embed_kp.set_image(url=kp_src)
            embed_kp.add_field(name='Profile Link', value=link, inline=False)

            await ctx.send(embed=embed_kp)
            break

@client.command(aliases=['supersecretcommandthatnobodywillknowbecauseitssolong'])
async def _supersecretcommandthatnobodywillknowbecauseitssolong(ctx):
    await ctx.send("Eunji ultimate bias 5 years poggers")

# @client.command(aliases=['opggteam'])
# async def _opggteam(ctx, *, msg):

@client.event
async def on_message(message):
    
    splt = str(message.author.display_name) #nickname
    # tag_id = str(message.author.id)         #discord ID
    msg_n = message.content.lower()    #message.content

    if 'is high' in msg_n: #easter egg
        await message.channel.send('https://www.youtube.com/watch?v=fpSTrry_5Fo')
        
    elif 'i love you eunji' in msg_n:
        await message.channel.send(f'i love you too {splt} :flushed:')
        await message.add_reaction('\N{HEAVY BLACK HEART}') 
        
    elif 'depressed' in msg_n:
        await message.channel.send(f"its ok {splt}, I'll be there for you")
        await message.channel.send('<:eunjiface:707716555538038875>')

    elif 'hug me' in msg_n:
        await message.channel.send(f'*hugs {splt}*')
        await message.channel.send('<:pandahug:707726416065593355>')

    elif 'thanks eunji' in msg_n:
        await message.channel.send(f"you're welcome {splt} :)")

    elif '<@!707455402744217610>' in msg_n:
        await message.channel.send("I'm busy right now :/ ping me again later")

    await client.process_commands(message)

@client.command(aliases=['helpme'])
async def _helpme(ctx):
    embed = discord.Embed(
        title = 'List of Commands',
        description = 'Bot Prefix: -',
        color = 0x65E1F0
    )
    embed.add_field(name='emb1', value='Posts Jeong Eunji', inline=False)
    embed.add_field(name='form1', value='Sends you a little form', inline=False)
    embed.add_field(name='goodnight', value='Sends you 1 out of 2 goodnight gif', inline=False)
    embed.add_field(name='latestcb', value='Sends the latest girl/girl group comeback', inline=False)
    await ctx.send(embed=embed)



client.run(token)