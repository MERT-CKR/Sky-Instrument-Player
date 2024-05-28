import time
import keyboard
import pandas as pd
import os
import json
import os



with open("settings.json", "r", encoding="utf-8") as file:
    data = json.load(file)

current_dir = os.getcwd()
translations_Path = os.path.join(current_dir,"translations.json")



# create path of New Sheets
directory = os.path.join(current_dir,"New Sheets")

# create folder
if not os.path.exists(directory):
    os.makedirs(directory)

def load_translations():
    global user_locale
    if data["settings"][0]["firstTime"] == 0 or data["settings"][0]["language"]=="":
        print("Select your language: \n1.Türkçe \n2.English")
        lang = int(input("\n>> "))
        if lang not in [1,2]:
            load_translations()
        if lang == 1:
            user_locale = "tr"
        elif lang == 2:
            user_locale = "en"

        data["settings"][0]["language"] = user_locale

        with open('settings.json', 'w', encoding="utf-8") as dosya:
            json.dump(data, dosya, indent=4,ensure_ascii=False)
    else:
        user_locale = data["settings"][0]["language"]


    with open(translations_Path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    global _
    _ = lambda key: translations['translations'][key][user_locale]

load_translations()



def update_settings():
    global data
    global newKeys
    global key
    
    if data["settings"][0]["firstTime"] == 1:
        pass
    else:
        print(_("first_opening"))
        unwanted_chars=["1","2","3","4","5","6","7","8","9","0","-","?","'","=","*","(",")","{","}"]
        unwanted_chars2=[".",","]

        print(_("tutorial1"))
        print(_("tutorial2"))

        newKeys = input(">> ")
        for keyx in newKeys:
            if keyx in unwanted_chars2:
                print(_("dot_comma_error"))
                update_settings()
            if keyx in unwanted_chars:
                invChar= _("invalid_char").replace("*",keyx)
                print(invChar)
                update_settings()
            elif len(newKeys) !=29:
                print(_("length_err"))
                update_settings()
                
        data["settings"][0]["firstTime"] = 1
        if newKeys == "":
            data["settings"][0]["keys"] = data["settings"][0]["Default_keys"]
        else:
            data["settings"][0]["keys"] = newKeys



    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(_("key_assigned"))
    key =  data["settings"][0]["keys"]
    key = key.split()

update_settings()

SheetKeys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]
key = key[::-1]

def normalizeJson(Fname):
    Fpath = os.path.join(current_dir, "New Sheets", Fname)
    
    # read JSON file
    with open(Fpath, 'r') as f:
        data = json.load(f)
    
    # Getting first element of JSON file
    if len(data) > 0 and isinstance(data[0], dict):
        song_data = data[0]
    else:
        ErrMsg = _("unknown_format")
        ErrMsg=ErrMsg.replace("*",Fname)
        raise ValueError(ErrMsg)

    # validation of "songNotes" key
    if "songNotes" in song_data:
        song_notes = song_data["songNotes"]
    else:
        ErrMsg = _("unknown_format2")
        ErrMsg=ErrMsg.replace("*",Fname)
        raise KeyError(ErrMsg)

    #Dictionary to hold merged data
    merged_data = {}

    # Processing data
    for item in song_notes:
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
    with open(os.path.join(current_dir, "Sheets", Fname), 'w', encoding="UTF-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    
def countDown():
    print(_("starting"))
    time.sleep(1)
    print(4)
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    




# Convert music to the correct format
file_list = os.listdir(os.path.join(current_dir, "New Sheets"))
for file in file_list:
    if file.endswith(".txt"):
        newName = file.replace(".txt", ".json")
        oldpath = os.path.join(current_dir, "New Sheets", file)
        newpath = os.path.join(current_dir, "New Sheets", newName)
        try:
            os.rename(oldpath, newpath)
            os.remove(oldpath)
        except Exception as e:
            pass

# Make the file more readable
file_list = os.listdir(os.path.join(current_dir, "New Sheets"))
for file in file_list:
    if file.endswith(".json"):
        normalizeJson(file)
        
        # clearing old note format file
        clr_list = os.listdir(os.path.join(current_dir, "New Sheets"))
        for i in clr_list:
            os.remove(os.path.join(current_dir, "New Sheets", i))
            
            

def Timer(function="return-timer"):
    global salise
    global now
    if function == "start":
        now = time.time()+1
        salise = int((now - int(now)) * 1000) 
        
    else:
        elapsed_time = time.time() - now 
        return salise + int(elapsed_time * 1000) 
            
def playMusic():
    global df1
    filepath = os.path.join(current_dir, "Sheets", selcted_music + ".json")
    df1 = pd.read_json(filepath)
    
    countDown()
    Timer("start") 
    for t in range(len(df1["time"])):
        note_time = df1["time"][t]
        current_time = Timer()  
        
        while current_time < note_time:  # wait for correct time
            current_time = Timer()

        if keyboard.is_pressed('"'):
            print(_("loop_ending"))
            break
        
        notes = df1["key"][t].split(",")
        notes_to_press = []
        for note in notes:
            pressed_keys = note.split(" ")
            for char in pressed_keys:
                char=char.replace("2Key","1Key").replace("3Key","1Key")
                char = char.strip()
                if char in SheetKeys:
                    index = SheetKeys.index(char)
                    key_to_press = key[index]  # Determine the key in the relevant index
                    notes_to_press.append(key_to_press)  # add notes to list
                else:
                    invalidChar=_("invalid_char")
                    invalidChar=invalidChar.replace("*",char)
                    print(invalidChar)
                    
        # Notes to be played simultaneously
        for key_to_press in notes_to_press:
            keyboard.press(key_to_press)
        print(notes_to_press)
        time.sleep(0.05)  # tuşlar arası bekleme.
        # Basılan notaları serbest bırak
        for key_to_press in notes_to_press:
            keyboard.release(key_to_press)

        if keyboard.is_pressed('"'):
            print(_("loop_ending"))
            break




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

def bring():
    global selcted_music
    global selection
    print(_("choose_music"))
    ShowList()
    
    err=0
    try:
        selection = int(input(">> "))
    except:
        err=1
    
    if err==1:
        print(_("type_error"))
        bring()
        
    if selection > max(Sheet_dict) or selection <=0:
        print(_("choose_in_list"))
        bring()
    else:
        selcted_music = Sheet_dict[selection]
        playMusic()



while True:
    bring()
    print(_("restart"))
    keepContinue = input(">> ")
    if keepContinue == "0":
        break
    else:
        continue








