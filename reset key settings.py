import json

new_data = {
    "settings": [
        {
            "firstTime": 0,
            "keys": "",


            "Default_keys": "y u ı o p h j k l ş n m ö ç b",
            "example": "q w e r t a s d f g z x c v b",
            "language": "tr"
            
        }
    ]
}

with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(new_data, file, indent=4, ensure_ascii=False)

print("key rest successfull.")