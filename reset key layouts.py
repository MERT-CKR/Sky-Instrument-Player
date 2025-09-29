import json
from pandas import read_json
import time
settings = read_json("settings.json")
version = settings["settings"][0]["version"]
#get version from settings


new_data = {
    "settings": [
        {
            "firstTime": 0,
            "keys": "",
            "Tr_keys": "y u ı o p h j k l ş n m ö ç b",
            "Example": "q w e r t a s d f g z x c v b",
            "language": "",
            "changelog":"",
            "version": version
            
        }
    ]
}

with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(new_data, file, indent=4, ensure_ascii=False)

print("key rest successfull.")
time.sleep(2)
