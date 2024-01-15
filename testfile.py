import os
from dotenv import load_dotenv
from pysteamgear import SteamAPI
from pysteamgear.modules import SteamData

load_dotenv()
api = SteamAPI(os.getenv('API_KEY'),'json')

data: SteamData = api.isteam_store.app_details(appid=606880)

print(data.headers)
print(data.title)

for d in data.items:
    print(d)
