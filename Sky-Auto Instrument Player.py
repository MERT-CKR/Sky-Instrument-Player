import os
import json
import requests


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



from modules.utils import load_translations
from modules.utils import print_red, print_yellow, print_green, print_colorful_list
from modules.utils import fix_old_format
_ = load_translations()
from modules.get_layout_and_scan_code import get_layout


if settings["firstTime"] != 1:
    
    #first_opening
    print(_("first_opening"))
    
    print_yellow(_("pass_without_layout"))
    print_green(_("add_sky_layout"))

    sky_key_layout = "" #input(">> ")
    options = {1:"nightly_layout", 
               2: "sky_layout"}

    print(options[1])
    keys = get_layout()

    if sky_key_layout == "":
        enable_sky_keys = False
    
    else:
        enable_sky_keys = True
        layouts["sky_layout"] = sky_key_layout

    settings["firstTime"] = 1
    with open(settings_path, 'w', encoding = "utf-8") as old_settings:
        json.dump({"settings": [settings]}, old_settings, indent = 4, ensure_ascii = False)

    print_yellow(_("key_assigned"))
    

if layouts["sky_layout"] == "":
    enable_sky_keys = False
else:
    enable_sky_keys = True



if enable_sky_keys:
    print_green(_("select_layout"))
    print_colorful_list(1, f"        Sky Music Nightly :  {layouts["nightly_layout"]}")
    print_colorful_list(2, f"Sky Children of the light :  {layouts["sky_layout"]}")
    selection = input(">> ")

    if selection == "1":
        key_layout = layouts["nightly_layout"]
    elif selection == "2":
        key_layout = layouts["sky_layout"]
        
else:
    key_layout = layouts["nightly_layout"]


# select layout
# ascii tuşlara basmayı ekle yoksa keyboard layout sikintisi loading

def check_Updates():
    print_yellow(_("checking_updates"))
    current_rel = settings["version"]

    url = "https://raw.githubusercontent.com/MERT-CKR/Sky-Instrument-Player/main/settings.json"
    connection = True
    try:
        response = requests.get(url, timeout=4)
    except requests.ConnectionError:
        print_red(_("connection_error"))
        connection = False

        
    if connection:
        try:
            json_content = response.json()
            json_content = json_content["settings"][0]
            new_rel = json_content["version"]
            changelog = json_content["changelog"]

            if new_rel == current_rel:
                print_green(_("using_latest_version"))
                
            elif new_rel > current_rel:
                new_ver = _("new_version_available").replace("*current_rel", current_rel).replace("*new_rel", new_rel)
                print_green(new_ver)

                if changelog != "":
                    print_green(_("changelog"))
                    print_yellow(changelog)
            else:
                print_yellow("Developing\n")
                print("Your version:", current_rel)
                print("Github version:", new_rel)

        except Exception as err:
            print_red(err)
            print_red(_("version_could_not_be_checked"))
            
check_Updates()


music_list = os.listdir(Sheets_path)
music_list = [m for m in music_list if m.endswith(".skysheet") or  m.endswith(".txt") or m.endswith(".json")]#remove unknown extensions
musicDict = {}



def return_notes(selection):

    selected_music = music_list[selection-1]
    selected_path = os.path.join(Sheets_path,selected_music)
    print(selected_music,selected_path)

    try:
        with open(selected_path, "r", encoding="utf-8") as sheet:
            sheet = json.load(sheet)
    except:
        with open(selected_path, "r", encoding="utf-16") as sheet:
            sheet = json.load(sheet)

    if "songNotes" in sheet[0]:
        sheet = sheet[0]["songNotes"]
        print_green(sheet)

    elif 'time' and 'key' in sheet[0].keys():
        print(_("old_format"))
        fix_old_format(sheet, selected_music, selected_path)


    # playeri çağır
    # sikintili nota formatlarını ve klasör yapısını düzelt
    # player genshindeki gibi boşluklu göstersin


def showList():
    counter = 0
    for item in music_list:
        ext = item.split(".")[1]
        item = item.replace("." + ext, "")#remove extension like .txt
        counter += 1
        print_colorful_list(counter, item)
    
    try:
        selection = int(input(f"\033[32m{_("choose_music")}\033[0m"))# green input message
    except:
        showList()
        return
    
    if selection > len(music_list) or selection <= 0:
        showList()
        return
    
    return_notes(selection)

    

while __name__ == "__main__":
    showList()
    print_green(_("restart"))
    keep_continue = input(">> ")


