import json

from discord.ext import commands
from client.newsapi_client import NewsApiClient
from client.darksky_api_client import DarkSkyClient

# Fetch all necessary information from news api client and populate an embedded message
news_api_client = NewsApiClient("")
news_api_response = news_api_client.make_news_api_request()
stories_to_urls = news_api_client.get_list_of_story_urls(news_api_response=news_api_response, number_of_stories=3)
news_api_discord_message = news_api_client.create_embedded_discord_message(stories=stories_to_urls)

# Fetch all necessary information from darksky client and populate an embedded message
darksky_client: DarkSkyClient = DarkSkyClient("")
darksky_response: json = darksky_client.make_dark_sky_request()
darksky_api_discord_message = darksky_client.create_embedded_discord_message(darksky_api_response=darksky_response)

bot: commands.Bot = commands.Bot(command_prefix="*", help_command=None)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="weather")
async def displayedembed(ctx):
    await ctx.send(embed=darksky_api_discord_message)


@bot.command(name="news")
async def displayedembed(ctx):
    await ctx.send(embed=news_api_discord_message)


if __name__ == "__main__":
    bot.run("")
