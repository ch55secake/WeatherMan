class NewsApiRequestException(Exception):
    """
    Exception for when reaching out to the News API fails.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        print(f"Request error whilst fetching news information from the News API.")
