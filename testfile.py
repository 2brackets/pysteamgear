import os
from dotenv import load_dotenv
from pysteamgear import SteamConfig
from pysteamgear.steam_interfaces import ISteamStore, ISteamNews
from pysteamgear.modules import SteamData

load_dotenv()
config = SteamConfig(os.getenv('API_KEY'),'json')

data: SteamData = ISteamStore.app_users_details(config=config, appid='440')

#data2: SteamData = ISteamNews.get_news_for_app(config=config, appid=606880, count=2)

print(data.content_type)
print(data.api)
print(data.title)
print(data.headers)
print(data.len_cookies)
print(data.len_headers)
print(data.len_items)
print(data.items[0])
print(data.content)
