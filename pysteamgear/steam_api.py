from .steam_interfaces import ISteamNews, ISteamStore

FORMATS = ['json', 'xml', 'vdf']

class SteamAPI():
    """
    The SteamAPI class provides an interface for interacting with the Steam Web API.

    Attributes:
        config (dict): A dictionary containing configuration settings for the API.

    Args:
        web_api_key (str): Your Steam Web API key.
        preferred_output_format (str, optional): The preferred format for API responses. 
            Defaults to 'json'. Valid formats are defined in the FORMATS variable.
        access_token (str, optional): The access token for user authentication. 
            Defaults to None.
        steam_id (str, optional): The Steam ID for the user. Defaults to None.
    """
    def __init__(self,
            web_api_key: str,
            preferred_output_format: str ='json',
            access_token: str =None,
            steam_id: str =None,
            time_out: int = 300):

        self._validate_format(preferred_output_format)

        self.config = {
            'key': web_api_key,
            'format': preferred_output_format,
            'token': access_token,
            'id': steam_id,
            'time': time_out
        }

        # Load all Steam api interfaces
        self.isteam_news = ISteamNews(self.config)
        self.isteam_store = ISteamStore(self.config)

    def _validate_format(self, output_format: str):
        if output_format not in FORMATS:
            raise ValueError(
                f"Invalid format: {output_format}. Valid formats are: {FORMATS}")

    def set_config(
            self, web_api_key: str = None, preferred_output_format: str =None,
            access_token: str =None, steam_id: str =None, time_out: int = None):
        """
        Update the SteamAPI configuration settings.

        Args:
            web_api_key (str, optional): New Steam Web API key.
            preferred_output_format (str, optional): New preferred output format for API responses.
            access_token (str, optional): New access token for user authentication.
            steam_id (str, optional): New Steam ID for the user.
        """
        new_config = {}
        if web_api_key is not None:
            new_config['key'] = web_api_key
        if preferred_output_format is not None:
            self._validate_format(preferred_output_format)
            new_config['format'] = preferred_output_format
        if access_token is not None:
            new_config['token'] = access_token
        if steam_id is not None:
            new_config['id'] = steam_id
        if time_out is not None:
            new_config['time'] = time_out
        self.config.update(new_config)
 