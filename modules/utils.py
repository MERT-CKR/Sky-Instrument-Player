# module: utils
import os
import json
import time
import pygetwindow as gw
import requests
current_dir = os.path.dirname(os.path.realpath(__file__))
translations_path = os.path.join(current_dir, "translations.json")
settings_path = os.path.join(current_dir, "settings.json")
supported_extensions = [".skysheet", ".txt", ".json"]


with open(settings_path, "r", encoding = "utf-8") as file:
    settings = json.load(file)
    settings = settings["settings"][0]


    
def load_translations():
    with open(translations_path, 'r', encoding = 'utf-8') as file:
        translations = json.load(file)
        translations = translations['translations']
        
    user_locale = settings["language"]
    return lambda key: translations[key][user_locale]

_ = load_translations()


def print_red(arg: str):
    """
    Print Red text in console color code: 31
    """
    print(f"\033[31m{arg}\033[0m")#red message



def print_green(arg: str):
    """
    Print Green text in console. color code: 32
    """
    print(f"\033[32m{arg}\033[0m")#green message



def print_yellow(arg: str):
    """
    Print Yellow text in console. color code: 33
    """
    print(f"\033[33m{arg}\033[0m")#yellow message



def print_colorful_list(index: any, item: str):
    """
    print colorfull list index and list item color codes: 93, 91
    """
    print(f"\033[93m{index}\033[0m \033[91m{item}\033[0m")

def countDown():
    print(4)
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(_("starting"))

def timer(function = 0):
    global salise
    global now
    if function == 1:
        now = time.time()
        salise = int((now - int(now)) * 1000)

    else:
        elapsed_time = time.time() - now
        return salise + int(elapsed_time * 1000)




def select_window():
    global target

    windows = gw.getAllTitles()
    windows = list(set(windows))
    
    # Clear the list to show users
    
    recommended = ["Sky", "Oynatıcı", "Player", "Pemain", "Reprodutor", "Плеер", "演奏器" ] # windows where these words appear
    unwanted = ["Sky-Auto Instrument Player", "Dosya Gezgini", "File Explorer", "Visual Studio Code", "Discord"]# Dont appear these
    windows = [win for win in windows if win != ""] # Remove empty list elements

    related_windows = []
    for window in windows:
        for recommend in recommended:
            if recommend in window:
                related_windows.append(window)

    related_windows.sort()

    for item in unwanted:
        related_windows = [win for win in related_windows if item not in win]


    if related_windows == []:
        window = 0
        target = None
        
    else:
        counter = 0
        print("\n")
        print_green(_("choose_window"))
        print_colorful_list("0", _("continue_without_selection"))
        for i in range(len(related_windows)):
            counter += 1
            print_colorful_list(counter, related_windows[i])

        try:
            choise = int(input(">> "))
        except Exception as e:
            print_red(e)
            select_window()
            return
        
        if choise != 0:
            target = related_windows[choise-1]
            window = gw.getWindowsWithTitle(target)[0]
            print_green(_("give_focus"))

            while gw.getActiveWindowTitle() != target:
                time.sleep(0.5)
            return target







def check_Updates():
    print_yellow(_("checking_updates"))
    current_rel = settings["version"]

    url = "https://raw.githubusercontent.com/MERT-CKR/Sky-Instrument-Player/main/modules/settings.json"
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












def check_number_of_layer(raw_sheet_file):
    try:
        if len(raw_sheet_file[0]["instruments"]) > 1:
            return False
        else: 
            return True
    except:
        return True
    
def fix_old_format(sheet, selected_music, selected_path):
    for ext in supported_extensions:
        if ext in selected_music:
            selected_music.replace(ext,"")

    fixed_songNotes = []
    for line in sheet:
        key = line["key"]
        time = line["time"]

        if "," not in key:
            fixed_songNotes.append({"key":key,"time":time})

        else:
            key = key.split(",")
            for k in key:
                fixed_songNotes.append({"key":k,"time":time})
    
    
    new_format = [{}]
    add_feature = new_format[0]
    add_feature["name"] = selected_music
    add_feature["bpm"] = 300
    add_feature["bitPerPage"] = 16
    add_feature["pitchLevel"] = 1
    add_feature["isComposed"] = False
    add_feature["songNotes"] = fixed_songNotes
    try:
        with open(selected_path, "w", encoding="utf-8") as old_format:
            json.dump(new_format, old_format, indent=4, ensure_ascii=False)
    except:
        with open(selected_path, "w", encoding="utf-16") as old_format:
            json.dump(new_format, old_format, indent=4, ensure_ascii=False)

    print(_("old_format_fixed"))
    print(new_format)
    # playMusic(new_format[0]["songNotes"])#ignore