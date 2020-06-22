import discord
from discord.ext import commands, tasks
from bot_commands.bot_commands import BotCommands
from cogs.management import Management

from secret_keys import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix = '~', activity = discord.Game("Eunji bot clone for testing"))

#bot m
@client.event
async def on_ready():
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

BotCommands(client)
client.add_cog(Management(client))

@client.event
async def on_message(message):
    
    print(f'Message from {message.author.id} in channel {message.channel.id} in server {message.guild.id}')
    print(message.content)

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


client.run(DISCORD_BOT_TOKEN)