import discord
from discord.ext import commands
import requests
import json

from secret_keys import OPENWEATHER_API_KEY

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, *, msg):

        sg = str(msg)

        city = sg.split()

        if len(city) > 1:
            city = sg.replace(' ', '&')

        elif len(city) == 1:
            city = ''.join(msg)

        else:
            print("you're ruining the purpose of this smh put in something")

        url =  f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'

        data = requests.get(url).json()

        weather = data['weather'][0]['main'] #weather
        weatherdesc = data['weather'][0]['description'] #weather description
        tempk = data['main']['temp'] # temperature in kelvin
        tempfs = data['main']['feels_like'] # feelslike temperature in kelvin
        humidity = data['main']['humidity']

        humidity = str(humidity) + '%'

        #conversion from kelvin into fahrenheit
        tempf = (tempk - 273.15) * 1.8 + 32 
        tempfeels = (tempfs - 273.15) * 1.8 + 32 
        
        carrot = round(tempf, 1), round(tempfeels, 1), weather,weatherdesc, humidity

        await ctx.send(carrot)