class DarkSkyRequestException(Exception):
    """
    Exception for when reaching out to the DarkSky API fails.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        print(f"Request error whilst fetching weather information from the DarkSky API.")
        return self.message
