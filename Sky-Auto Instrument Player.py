import os
import json


current_dir = os.getcwd()
Sheets_path = os.path.join(current_dir,"Sheets")
supported_extensions = [".skysheet", ".txt", ".json"]
settings_path = os.path.join(current_dir, "modules", "settings.json")
layouts_path = os.path.join(current_dir, "modules", "key_layouts.json")


with open(settings_path, "r", encoding = "utf-8") as file:
    settings = json.load(file)
    settings = settings["settings"][0]

with open(layouts_path, "r", encoding = "utf-8") as file:
    layouts = json.load(file)
    layouts = layouts["layouts"][0]


lang_dict = {
    "1" : "tr",
    "2" : "en"
}

supported_languages = list(lang_dict.values())
supported_lang_index = lang_dict.keys()
user_locale = settings["language"]


if user_locale not in supported_languages:
    print(f"\033[32mSelect your language:\033[0m")
    counter = 0
    for item in supported_languages:
        counter += 1
        print(f"\033[93m{counter}\033[0m \033[91m{item}\033[0m") #Colorfull list
    input_lang_index = input(">> ")
    
    if input_lang_index in supported_lang_index:
        selected_lang = lang_dict[input_lang_index]

        if selected_lang in supported_languages:
            user_locale = selected_lang

    else:
        raise ValueError(f"Language not selected \nOptions are {supported_languages} !!!")
    

    settings["language"] = user_locale
    

    with open(settings_path, 'w', encoding = "utf-8") as old_file:
        json.dump({"settings": [settings]}, old_file, indent = 4, ensure_ascii = False)




from modules.utils import load_translations, print_red, print_yellow, print_green, print_colorful_list, fix_old_format, check_number_of_layer, check_Updates
_ = load_translations()

from modules.get_scan_code import get_layout
from modules.player_core import playMusic



if layouts["sky_game_layout"] == {}:
    keys = get_layout(layout_name = "sky_game_layout")

if settings["ask_for_nightly_layout"] == 1:
    if layouts["sky_music_nightly_layout"] == {}:
        print_yellow("if you using sky music nightly you can add the layout")

        print_colorful_list("1", "Add")
        print_colorful_list("2", "Ask Later")
        print_colorful_list("3", "Skip and don't ask")
        selection = input(">> ")
        
        if selection == "1":
            keys = get_layout(layout_name = "sky_music_nightly_layout")
        
        elif selection =="2":
            pass

        else:
            settings["ask_for_nightly_layout"] = 0
            with open(settings_path, 'w', encoding = "utf-8") as old_file:
                json.dump({"settings": [settings]}, old_file, indent = 4, ensure_ascii = False)

with open(layouts_path, "r", encoding = "utf-8") as file:
    layouts = json.load(file)
    layouts = layouts["layouts"][0]

printable_nightly_key = str(list(layouts["sky_music_nightly_layout"].keys())).replace("'", "").replace(",","")
printable_sky_key = str(list(layouts["sky_game_layout"].keys())).replace("'", "").replace(",","")

available_keys_dict = {
    "nightly" : printable_nightly_key,
    "sky" : printable_sky_key
}

if available_keys_dict["nightly"] == str([]):
    
    key_layout = layouts["sky_game_layout"]

else:
    print_green(_("select_layout"))
    print_colorful_list(1, f"        Sky Music Nightly :  {printable_nightly_key}")
    print_colorful_list(2, f"Sky Children of the light :  {printable_sky_key}")
    selection = input(">> ")

    if selection == "1":
        key_layout = layouts["sky_music_nightly_layout"]

    elif selection == "2":
        key_layout = layouts["sky_game_layout"]


            
check_Updates()


music_list = os.listdir(Sheets_path)
music_list = [m for m in music_list if m.endswith(".skysheet") or  m.endswith(".txt") or m.endswith(".json")]#remove unknown extensions
musicDict = {}



def return_notes(selection):
    selected_music = music_list[selection-1]
    selected_path = os.path.join(Sheets_path,selected_music)

    try:
        with open(selected_path, "r", encoding="utf-8") as sheet:
            sheet = json.load(sheet)
            raw_sheet = sheet.copy()
    except:
        with open(selected_path, "r", encoding="utf-16") as sheet:
            sheet = json.load(sheet)
            raw_sheet = sheet.copy()

    if "songNotes" in sheet[0]:
        sheet = sheet[0]["songNotes"]
        
        if check_number_of_layer(raw_sheet): # it not support multiple layer
            playMusic(sheet, key_layout)
        else:
            print_red(_("multiple_layer_detected"))


    elif 'time' and 'key' in sheet[0].keys():
        print(_("old_format"))
        fix_old_format(sheet, selected_music, selected_path)

    else:
        print(_("unknown_format"))



def showList():
    counter = 0
    for item in music_list:
        ext = item.split(".")[1]
        item = item.replace("." + ext, "")# remove extension to show user
        counter += 1
        print_colorful_list(counter, item)
    
    try:
        selection = int(input(f"\033[32m{_("choose_music")}\033[0m"))
    except:
        showList()
        return
    
    if selection > len(music_list) or selection <= 0:
        print_red(_("choose_in_list"))
        showList()
        return
    
    return_notes(selection)

    

while __name__ == "__main__":
    showList()
    print_green(_("restart"))
    keep_continue = input(">> ")


