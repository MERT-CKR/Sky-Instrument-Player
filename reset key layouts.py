import json
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
        }
    ]
}

with open("modules\\settings.json", "w", encoding="utf-8") as file:
    json.dump(settings, file, indent=4, ensure_ascii=False)

with open("modules\\key_layouts.json", "w", encoding="utf-8") as file:
    json.dump(layouts, file, indent=4, ensure_ascii=False)

print("key layouts have been reset.")
time.sleep(2)