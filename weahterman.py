import json
import random
import discord
from discord.ext import commands
from discord.utils import get
import time
import requests

url = "https://dark-sky.p.rapidapi.com/"

querystring = {"units": "auto", "lang": "en"}

headers = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "dark-sky.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

savedWeather = response.json()
dailySaved = (savedWeather["hourly"])
currentSummary = (dailySaved["summary"])
dailyData = (dailySaved["data"])
currentTemp = (dailyData[1]["temperature"])
windSpeed = (dailyData[1]["windSpeed"])

url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=ae05c4e7fd9145bf9b0a941fd4832443')
response = requests.get(url)
newsMoments = response.json()
storyOne = (newsMoments["articles"][0]["url"])
storyTwo = (newsMoments["articles"][1]["url"])
storyThree = (newsMoments["articles"][2]["url"])
publishOne = (newsMoments["articles"][0]["publishedAt"])
publishTwo = (newsMoments["articles"][0]["publishedAt"])
publishThree = (newsMoments["articles"][0]["publishedAt"])

bot = commands.Bot(command_prefix="*", help_command=None)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="weather")
async def displayedembed(ctx):
    embed = discord.Embed(title="🌎 Weather 🌎", color=0xff00ea)
    embed.add_field(name="Current Temperature(in Celsius)", value=currentTemp, inline=True)
    embed.add_field(name="Current Wind Speed", value=windSpeed, inline=True)
    embed.add_field(name="Summary", value=currentSummary, inline=True)
    embed.set_footer(text="Data provided by DarkWeather API.")
    await ctx.send(embed=embed)


@bot.command(name="news")
async def displayedembed(ctx):
    embed = discord.Embed(title="🌎 News 🌎", color=0xff00ea)
    embed.add_field(name="Breaking:", value=storyOne, inline=False)
    embed.add_field(name="Published at:", value=publishOne, inline=False)
    embed.add_field(name="Breaking:", value=storyTwo, inline=False)
    embed.add_field(name="Published at:", value=publishTwo, inline=False)
    embed.add_field(name="Breaking:", value=storyThree, inline=False)
    embed.add_field(name="Published at:", value=publishThree, inline=False)
    embed.set_footer(text="Data provided by the BBC.")
    await ctx.send(embed=embed)

bot.run("")
