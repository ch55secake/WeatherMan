import json

import discord as d
import requests as req

from exception.newsapi_request_exception import NewsApiRequestException


class NewsApiClient(object):

    def __init__(self, api_key: str):
        """
        Create a class that will reach out to a news api and get top stories.
        :param api_key: api key used for interacting with the news api
        """
        self.api_key = api_key

    def make_news_api_request(self):
        """
        Reaches out to news api with provided api key
        :return: news api response as json.
        """
        news_api_url: str = f"https://newsapi.org/v2/top-headlines?sources-bbc-news&apiKey={self.api_key}"
        try:
            return req.get(url=news_api_url).json()
        except req.exceptions.Timeout:
            print(f"Timeout whilst making request to News API")
        except req.exceptions.RequestException as e:
            raise NewsApiRequestException(e.request)

    @staticmethod
    def get_list_of_story_urls(news_api_response: json, number_of_stories: int) -> dict[str, str]:
        """
        Parses News API response in order to provide dict of URLs for later bot response
        :param news_api_response: json object from the news api
        :param number_of_stories: the number of story urls to fetch
        :return: dictionary of urls sorted by the publishing time
        """
        stories: dict[str, str] = {}
        for x in range(0, number_of_stories):
            stories.update({news_api_response["articles"][x]["publishedAt"], news_api_response["articles"][x]["url"]})

        return stories

    @staticmethod
    def create_embedded_discord_message(stories: dict) -> d.Embed:
        """
        Create embedded discord message with response from the news api
        :param stories: stories returned by the news api
        :return: discord embedded message populated with information from the news api
        """
        embed: d.Embed = d.Embed(title="🌎 News 🌎", color=0xff00ea)
        for published_at, story_url in stories.items():
            embed.add_field(name="Breaking:", value=story_url, inline=False)
            embed.add_field(name="Published at:", value=published_at, inline=False)

        embed.set_footer(text="Data provided by the BBC.")
        return embed
