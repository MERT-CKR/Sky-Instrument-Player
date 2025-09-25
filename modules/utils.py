import os
import json
import time
import pygetwindow as gw
# module: utils

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
    windows = [win for win in windows if win != ""]
    windows = [win for win in windows if "Sky-Auto Instrument Player" not in win]

    recommended = ["Sky", "Oynatıcı", "Player"]

    related_windows = []

    for window in windows:
        for recommend in recommended:
            if recommend in window:
                related_windows.append(window)


    if related_windows == []:
        window = 0
        target = None
        
    else:
        counter = 0
        print(_("continue_without_selection"))
        for i in range(len(related_windows)):
            counter+=1
            print(counter,related_windows[i])
        try:
            choise = int(input(_("choose_window")))
        except:
            select_window()
            return
        
        if choise == 0:
            target = None
            return countDown()
        else:
            target = related_windows[choise-1]
            window = gw.getWindowsWithTitle(target)[0]
            # try:
            #     gw.activate(window)
            # except:
            #     pass

            
            print(_("give_focus"))
            while gw.getActiveWindowTitle() != target:
                time.sleep(1)
                print(gw.getActiveWindowTitle(),target)
    return target

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