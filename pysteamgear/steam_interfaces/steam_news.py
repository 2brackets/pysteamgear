from ..http_client import HttpClient
from ..modules import SteamData

BAS_URL_STEAM = 'https://api.steampowered.com'
BAS_URL_PARTNER = 'https://partner.steam-api.com'

class ISteamNews():
    """
    A class to interact with the Steam News API.

    This class provides methods to retrieve news for a specific app from the Steam News API.

    Attributes:
        config (dict): Configuration settings including API key, request format, and timeout.
    """
    def __init__(self, config: dict) -> None:
        """
        Initializes the ISteamNews object with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        self.config = config

    def get_news_for_app(self,
            appid: int,
            maxlength: int = None,
            enddate: int = None,
            count:int=None,
            feed:str=None) -> SteamData:
        """
        Retrieves news for a specific app using the public Steam News API.

        Notes: public API

        Args:
            appid (int, Required): AppID to retrieve news for.
            maxlength (int, optional): Maximum length for the content to return, 
            if this is 0 the full content is returned,if it's less then a blurb is generated to fit.
            enddate (int, optional): Retrieve posts earlier than this date (unix epoch timestamp)
            count (int, optional): # of posts to retrieve (default 20).
            feed (str, optional): Comma-separated list of feed names to return news for

        Returns:
            SteamData: An object containing the response data from the Steam News API.
        """

        return HttpClient.get(
            url=f'{BAS_URL_STEAM}/ISteamNews/GetNewsForApp/v2/',
            params={
                'appid': appid,  
                'maxlength': maxlength,
                'enddate': enddate,
                'count': count,
                'feed': feed,
                'format': self.config.get('format') 
            },
            headers=None,
            timeout=self.config['time']
        )

    def get_news_for_app_authed(self,
            appid: int,
            maxlength: int = None,
            enddate: int = None,
            count:int=None,
            feed:str=None) -> SteamData:
        """
        Retrieves news for the specified app.
        Publisher only version that can return info for unreleased games.

        This method requires an API key for authentication.

        Notes: Partner API

        Args:
            appid (int, Required): AppID to retrieve news for.
            maxlength (int, optional): Maximum length for the content to return, 
            if this is 0 the full content is returned,if it's less then a blurb is generated to fit.
            enddate (int, optional): Retrieve posts earlier than this date (unix epoch timestamp)
            count (int, optional): # of posts to retrieve (default 20).
            feed (str, optional): Comma-separated list of feed names to return news for

        Returns:
            SteamData: An object containing the response data from the Steam News API.
        """

        return HttpClient.get(
            url=f'{BAS_URL_PARTNER}/ISteamNews/GetNewsForAppAuthed/v2/',
            params={
                'appid': appid,  
                'maxlength': maxlength,
                'enddate': enddate,
                'count': count,
                'feed': feed,
                'format': self.config.get('format')
            },
            headers={
            'x-webapi-key': self.config.get('key')
            },
            timeout=self.config['time']
        )
    