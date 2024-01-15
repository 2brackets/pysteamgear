from ..http_client import HttpClient
from ..modules import SteamData

BAS_URL_STORE = 'https://store.steampowered.com'
#BAS_URL_PARTNER = 'https://partner.steam-api.com'

class ISteamStore():

    def __init__(self, config: dict) -> None:
        """
        Initializes the ISteamStore object with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        self.config = config

    def app_details(self, appid:int, filters:str=None, cc:str=None, language:str=None) -> SteamData:
        return HttpClient.get(
            url=f'{BAS_URL_STORE}/api/appdetails',
            params={
                'appids': appid,  
                'filters': filters,
                'cc': cc,
                'language': language, 
            },
            headers=None,
            timeout=self.config['time']
        )
    