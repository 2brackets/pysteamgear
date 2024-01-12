from pysteamgear import SteamAPI

api = SteamAPI('111','json')

print(api.isteam_news.get_news_for_app(appid=440, count=2))


