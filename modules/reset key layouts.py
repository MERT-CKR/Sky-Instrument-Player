import json
<<<<<<< HEAD
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
            
=======
import time

with open("modules\\settings.json", "r", encoding="utf-8") as file:
    settings = json.load(file)
    try:
        settings = settings["settings"][0]
        version = settings["version"]
        #get version from settings
    except:
        version = "1.1"
        pass




settings = {
    "settings": [
        {
            "ask_for_nightly_layout": 1,
            "language": "en",
            "changelog": "",
            "version": version
        }
    ],
}

layouts = {
    "layouts": [
        {
            "sky_music_nightly_layout": {
            },
            "sky_game_layout": {
                
            }
>>>>>>> origin/Dev
        }
    ]
}

<<<<<<< HEAD
with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(new_data, file, indent=4, ensure_ascii=False)

print("key rest successfull.")
time.sleep(2)
=======
with open("modules\\settings.json", "w", encoding="utf-8") as file:
    json.dump(settings, file, indent=4, ensure_ascii=False)

with open("modules\\key_layouts.json", "w", encoding="utf-8") as file:
    json.dump(layouts, file, indent=4, ensure_ascii=False)

print("key layouts have been reset.")
time.sleep(2)
>>>>>>> origin/Dev
