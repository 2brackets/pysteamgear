import requests

BAS_URL_STEAM = 'https://api.steampowered.com/'
BAS_URL_PARTNER = 'https://partner.steam-api.com/'

class ISteamNews():
    def __init__(self, config: dict) -> None:
        self.config = config

    def get_news_for_app(self,
            appid: int,
            maxlength: int = None,
            enddate: int = None,
            count:int=None,
            feed:str=None) -> str:

        url = f'{BAS_URL_STEAM}ISteamNews/GetNewsForApp/v2/'

        params = {
            "appid": appid,  
            "maxlength": maxlength,
            'enddate': enddate,
            "count": count,
            'feed': feed,
            "format": self.config.get('format') 
        }

        resp = requests.get(url=url, params=params, timeout=self.config['time'])

        return resp.text
    