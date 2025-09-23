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
            "firstTime": 0,
            "language": "",
            "changelog": "",
            "version": version
        }
    ],
}

layouts = {
    "layouts": [
        {
            "nightly_layout": {
                "q": 16,
                "w": 17,
                "e": 18,
                "r": 19,
                "t": 20,
                "a": 30,
                "s": 31,
                "d": 32,
                "f": 33,
                "g": 34,
                "z": 44,
                "x": 45,
                "c": 46,
                "v": 47,
                "b": 48
            },
            "sky_layout": {},
            "tr_keys": "y u ı o p h j k l ş n m ö ç ."
        }
    ]
}

with open("modules\\settings.json", "w", encoding="utf-8") as file:
    json.dump(settings, file, indent=4, ensure_ascii=False)

with open("modules\\key_layouts.json", "w", encoding="utf-8") as file:
    json.dump(layouts, file, indent=4, ensure_ascii=False)

print("key layouts have been reset.")
time.sleep(2)