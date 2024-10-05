import json

import discord as d
import requests as req

from exception.darksky_request_exception import DarkSkyRequestException


class DarkSkyClient(object):

    def __init__(self, api_key: str):
        """
        Basic client for interacting with the DarkSky weather api
        :param api_key: API Key required for interacting with DarkSky API
        """
        self.api_key = api_key

    def make_dark_sky_request(self):
        """
        Make request to DarkSky api with provided key and parameters
        :return: Json response object from DarkSky API
        :raises: DarkSkyRequestException
        :rtype:  Json
        """
        darksky_url = "https://dark-sky.p.rapidapi.com/"
        try:
            response = req.get(darksky_url, headers=self.headers(), params=self.create_query_params("auto", "en"))
            return response.json()
        except req.exceptions.Timeout:
            print(f"Timeout whilst making request to DarkSky API")
        except req.exceptions.RequestException as e:
            raise DarkSkyRequestException(e.strerror)

    def headers(self) -> dict[str, str]:
        """
        Creates headers required for interacting with the darksky api.
        :return: dictionary of headers
        """
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "dark-sky.p.rapidapi.com"
        }

    @staticmethod
    def get_daily_weather_info(darksky_api_response: json) -> tuple[any, any]:
        """
        Get weather data from the response of the DarkSky api.
        :param darksky_api_response: response received from the DarkSky api.
        :return: tuple that contains the current summary of the day and the daily data.
        """
        return darksky_api_response["hourly"]["summary"], darksky_api_response["hourly"]["data"]

    @staticmethod
    def create_query_params(units: str, lang: str) -> dict[str, str]:
        """
        Create query parameters used for reaching out to the DarkSky api.
        :param lang: the language you want the response to return
        :param units, decides what units the response will contain, e.g Fahrenheit or Celsius
        :return: dictionary of query parameters
        """
        return {
            "units": units,
            "lang": lang
        }

    def create_embedded_discord_message(self, darksky_api_response: json) -> d.Embed:
        """
        Create embedded discord message, will use data from darksky api in order to populate this
        :param darksky_api_response: original response used to populate the message
        :return: discord embedded message
        """
        embed: d.Embed = d.Embed(title="🌎 Weather 🌎", color=0xff00ea)
        summary, daily_data = self.get_daily_weather_info(darksky_api_response=darksky_api_response)
        wind_speed, current_temp = daily_data[1]["temperature"], daily_data[1]["windSpeed"]
        embed.add_field(name="Current Temperature(in Celsius)", value=current_temp, inline=True)
        embed.add_field(name="Current Wind Speed", value=wind_speed, inline=True)
        embed.add_field(name="Summary", value=summary, inline=True)
        embed.set_footer(text="Data provided by DarkWeather API.")
        return embed
