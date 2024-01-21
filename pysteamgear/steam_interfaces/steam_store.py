from ..http_client import HttpClient
from ..modules import SteamData
from ..steam import Steam

BAS_URL_STORE = 'https://store.steampowered.com'
#BAS_URL_PARTNER = 'https://partner.steam-api.com'

class ISteamStore():

    @staticmethod
    def app_details(config: Steam,
                    appid:int,
                    filters:str=None,
                    cc:str=None,
                    language:str=None) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/api/appdetails',
            params={
                'appids': appid,  
                'filters': filters,
                'cc': cc,
                'language': language, 
            },
            headers={'Accept': config.headers_format},
            timeout=config.timeout
        )

    @staticmethod
    def app_users_details(config: Steam, appid:int) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/api/appuserdetails',
            params={
                'appids': appid 
            },
            headers={
                'Accept': config.headers_format,
                'x-webapi-key': config.key
                },
            timeout=config.timeout
        )

    @staticmethod
    def get_store_categories(config: Steam) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/actions/ajaxgetstorecategories',
            params=None,
            headers={'Accept': config.headers_format},
            timeout=config.timeout
        )

    @staticmethod
    def get_store_tags(config: Steam) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/actions/ajaxgetstoretags',
            params=None,
            headers={'Accept': config.headers_format},
            timeout=config.timeout
        )

    @staticmethod
    def resolve_bundles(config: Steam,
                        bundle_ids: int,
                        cc: str,
                        l: str,
                        origin: str = None) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/actions/ajaxresolvebundles',
            params={
                'bundleids': bundle_ids,
                'cc': cc,
                'l': l,
                'origin': origin
            },
            headers={'Accept': config.headers_format},
            timeout=config.timeout
        )

    @staticmethod
    def resolve_packages(config: Steam,
                        package_ids: int,
                        cc: str,
                        l: str,
                        origin: str = None) -> SteamData:

        return HttpClient.get(
            url=f'{BAS_URL_STORE}/actions/ajaxresolvepackages',
            params={
                'packageids': package_ids,
                'cc': cc,
                'l': l,
                'origin': origin
            },
            headers={'Accept': config.headers_format},
            timeout=config.timeout
        )
       