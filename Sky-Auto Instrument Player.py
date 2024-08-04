import shutil
import time
import os
import json
from keyboard import is_pressed,press,release
from pandas import read_json
import requests

with open("settings.json", "r", encoding="utf-8") as file:
    data = json.load(file)

current_dir = os.getcwd()
translations_path = os.path.join(current_dir,"translations.json")


# Create path of New Sheets
directory = os.path.join(current_dir,"New Sheets")
directory2 = os.path.join(current_dir,"Raw Sheets")

# Create folder
if not os.path.exists(directory):
    os.makedirs(directory)

if not os.path.exists(directory2):
    os.makedirs(directory2)



def load_translations():
    global user_locale
    if data["settings"][0]["firstTime"] == 0 or data["settings"][0]["language"]=="":
        print("Select your language: \n1.Türkçe \n2.English")
        lang = input("\n>> ")
        try:
            lang = int(lang)
        except:
            print(f"You can only enter numbers here: ({lang}) is not number")
            load_translations()
            return
        
        if lang not in [1,2]:
            print(f"please choose in list: {lang} not in list")
            load_translations()
            return
        
        if lang == 1:
            user_locale = "tr"
        elif lang == 2:
            user_locale = "en"

        data["settings"][0]["language"] = user_locale

        with open('settings.json', 'w', encoding="utf-8") as dosya:
            json.dump(data, dosya, indent=4, ensure_ascii=False)
    else:
        user_locale = data["settings"][0]["language"]


    with open(translations_path, 'r', encoding='UTF-8') as f:
        translations = json.load(f)

    global _
    _ = lambda key: translations['translations'][key][user_locale]

load_translations()





def check_Updates():
    print(_("Checking_updates"))
    settings = read_json("settings.json")
    current_rel = settings["settings"][0]["version"]

    url ="https://raw.githubusercontent.com/MERT-CKR/Sky-Instrument-Player/main/settings.json"
    
    connection =True
    try:
        response = requests.get(url,timeout=10)
    except requests.ConnectionError:
        print(_("Connection_error"))
        connection=False

        
    if connection:
        try:
            json_content = response.json()
            new_rel = json_content["settings"][0]["version"]


            if new_rel==current_rel:
                print(_("using_last_version"))
                
            elif new_rel>current_rel:
                new_ver = _("new_version_available").replace("*current_rel",current_rel).replace("*new_rel",new_rel)
                print(new_ver)
                
        except Exception as e:
            print(_("version_could_not_be_checked"))
            


    
check_Updates()


def updateSettings():
    global key
    
    if data["settings"][0]["firstTime"] != 1:
        
        print(_("first_opening"))
        unwanted_chars=["1","2","3","4","5","6","7","8","9","0","-","?","'","=","*","(",")","{","}"]#can press these: '\' and '/'
        unwanted_chars2=[".",","]

        print(_("tutorial1"))
        print(_("tutorial2"))

        new_keys = input(">> ")
        for keyx in new_keys:
            if keyx in unwanted_chars2:
                print(_("dot_comma_error"))
                updateSettings()# Recursive exception handling
                return
            
            if keyx in unwanted_chars:
                invChar= _("invalid_char").replace("*",keyx)
                print(invChar)
                updateSettings()
                return
            
            elif len(new_keys) !=29:
                print(_("length_err"))
                updateSettings()
                return
                
        data["settings"][0]["firstTime"] = 1
        if new_keys == "":
            data["settings"][0]["keys"] = data["settings"][0]["Example"]
        else:
            data["settings"][0]["keys"] = new_keys


    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(_("key_assigned"))
    key =  data["settings"][0]["keys"]
    key = key.split()

updateSettings()


def normalizeJson(file_pth):
    file_name = file_pth.split("\\")[-1]
    
    
    # if file cant read with UTF-8 then try UTF-16
    try:
        with open(file_pth, 'r', encoding = "UTF-8") as f:
            data = json.load(f)
            
    except:
        with open(file_pth, 'r', encoding = "UTF-16") as f:
            data = json.load(f)
    
    
    # Get first element of JSON file
    if len(data) > 0 and isinstance(data[0], dict):
        song_data = data[0]
        
    else:
        # This method lets you replace something from translation
        err_msg = _("unknown_format").replace("*",file_name)
        raise ValueError(err_msg)

    # validation of "songNotes" key
    if "songNotes" in song_data:
        song_notes = song_data["songNotes"]
        
    else:
        err_msg = _("unknown_format2").replace("*",file_name)
        raise KeyError(err_msg)
    
    
    # Dictionary to hold merged data
    merged_data = {}

    # Change Sheet format
    for item in song_notes:
        item["key"] = item["key"].replace("2Key","1Key").replace("3Key","1Key")
        if 'time' in item and 'key' in item:
            time = item['time']
            key = item['key']
            if time not in merged_data:
                merged_data[time] = []
            merged_data[time].append(key)
        else:
            raise KeyError(_('key_error1'))

    # Converting results to merged format
    result = [{'time': time, 'key': ','.join(keys)} for time, keys in merged_data.items()]
    
    # write json file
    with open(os.path.join(current_dir, "Sheets", file_name), 'w', encoding="UTF-16") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    log_msg = _("added_list").replace("*",file_name.split(".")[0])
    print(log_msg)
    
sheets_dir = os.path.join(current_dir, "Sheets")
new_sheets_dir = os.path.join(current_dir, "New Sheets")

# Convert music to the wanted format
file_list = os.listdir(new_sheets_dir)
if file_list !=[]:
    for file in file_list:
        file_ext = file.split(".")[-1]
        if file_ext in ["skysheet","txt","json"]:
            new_file_name = file.replace(f".{file_ext}",".json")
            old_path = os.path.join(new_sheets_dir, file)
            new_path = os.path.join(new_sheets_dir, new_file_name)
            os.rename(old_path, new_path)
            
            normalizeJson(new_path)
            Sheets_list = os.listdir(sheets_dir)
            # Clearing old note format file
            if new_file_name in Sheets_list:
                shutil.copy(os.path.join(new_sheets_dir, new_file_name),os.path.join(current_dir, "Raw Sheets"))
                os.remove(os.path.join(new_sheets_dir, new_file_name))

        elif "." not in file:
            print(_("without_extension"))
            
        else:
            file = file.split(".")[-1]
            err = _("unwanted_format").replace("*",file)
            print(err)
            
        
            

def countDown():
    print(_("starting"))
    time.sleep(1)
    print(4)
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1,"\n")   
        

def timer(function="return-timer"):
    global salise
    global now
    if function == "start":
        now = time.time()
        salise = int((now - int(now)) * 1000)

    else:
        elapsed_time = time.time() - now 
        return salise + int(elapsed_time * 1000)

sheet_keys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]
key = key[::-1]          

def playMusic(selcted_music):
    filepath = os.path.join(current_dir, "Sheets", selcted_music + ".json")
    try:
        df1 = read_json(filepath)
    except:
        df1 = read_json(filepath, encoding='utf-16')
        
    counter = 1
    countDown()
    t1 = time.time()
    first_time = 0
    for t in range(len(df1["time"])):
        note_time = df1["time"][t]
        if first_time == 0:
            timer("start") 
            first_time = 1

        current_time = timer()
        while current_time < note_time:  # Wait for correct time
            current_time = timer()

        if is_pressed('"'):
            print(_("loop_ending"))
            break
        
        notes = df1["key"][t].split(",")
        
        notes_to_press = []
        for note in notes:
            pressed_keys = note.split(" ")
            for char in pressed_keys:
                char = char.strip()
                if char in sheet_keys:
                    index = sheet_keys.index(char)
                    key_to_press = key[index]  # Determine the key in the relevant index
                    notes_to_press.append(key_to_press)  # Add notes to list
                else:
                    invalid_char=_("invalid_char")
                    invalid_char=invalid_char.replace("*", char)
                    print(invalid_char)
                    
        # Notes to be play
        for key_to_press in notes_to_press:
            press(key_to_press)
        print(counter,notes_to_press)
        time.sleep(0.05)  # wait between per pres
        # Release pressed keys
        for key_to_press in notes_to_press:
            release(key_to_press)
        counter+=1
        
    t2=time.time()
    playtime = str(t2-t1)[0:4]
    play_duration =_("playback_duration")
    play_duration = play_duration.replace("*", playtime)
    print(play_duration)



Sheet_dict = {}

def ShowList():
    global counter
    counter = 1
    for file in os.listdir(os.path.join(current_dir, "Sheets")):
        if file.endswith(".json"):
            file = file.replace(".json", "")
            Sheet_dict[counter] = file
            print(counter, file)
            counter += 1

def main():
    global selection
    print(_("choose_music"))
    ShowList()

    try:
        selection = int(input(">> "))
    except TypeError:
        print(_("type_error"))
        main()
        return

    if selection > max(Sheet_dict) or selection <=0:
        print(_("choose_in_list"))
        main()
    else:
        selcted_music = Sheet_dict[selection]
        playMusic(selcted_music)


while __name__ == "__main__":
    main()
    print(_("restart"))
    keep_continue = input(">> ")
    if keep_continue == "0":
        break