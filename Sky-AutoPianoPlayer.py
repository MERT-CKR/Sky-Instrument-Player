import time
import keyboard
import pandas as pd
import os
import json



with open("settings.json", "r", encoding="utf-8") as file:
    data = json.load(file)

current_dir = os.getcwd()
translations_Path = os.path.join(current_dir,"translations.json")

def load_translations():
    if data["settings"][0]["firstTime"] == 0 or data["settings"][0]["language"]=="":
        print("Select your language: \n1.Türkçe \n2.English")
        lang = int(input("\n>> "))
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

# settings.json'u güncelle
if data["settings"][0]["firstTime"] == 1:
    pass
else:
    print(_("first_opening"))

    data["settings"][0]["firstTime"] = 1

    print(_("tutorial1"))
    # print(_("tutorial2"))
    # print(_("tutorial3"))
    # print(_("tutorial4"))

    newKeys = input(">> ")
    newKeys = newKeys.replace(",", " ")

    if newKeys == "":
        data["settings"][0]["keys"] = data["settings"][0]["Default_keys"]
    else:
        data["settings"][0]["keys"] = newKeys



with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(_("key_assigned"))
key =  data["settings"][0]["keys"]
key = key.split()





def normalizeJson(Fname):
    Fpath = os.path.join(current_dir, "New Sheets", Fname)
    
    # JSON dosyasını okuma
    with open(Fpath, 'r') as f:
        data = json.load(f)
    
    # JSON dosyasının ilk öğesini alma
    if len(data) > 0 and isinstance(data[0], dict):
        song_data = data[0]
    else:
        raise ValueError(f'{Fname} için hata: JSON dosyası beklenilen formatta değil.')

    # "songNotes" anahtarını doğrulama
    if "songNotes" in song_data:
        song_notes = song_data["songNotes"]
    else:
        raise KeyError(f'{Fname} için hata: "songNotes" anahtarı JSON dosyasında bulunamadı.')

    # Birleştirilmiş veriyi tutacak sözlük
    merged_data = {}

    # Verileri işleme
    for item in song_notes:
        if 'time' in item and 'key' in item:
            time = item['time']
            key = item['key']
            if time not in merged_data:
                merged_data[time] = []
            merged_data[time].append(key)
        else:
            raise KeyError(_('key_error1'))

    # Sonuçları birleştirilmiş formata çevirme
    result = [{'time': time, 'key': ','.join(keys)} for time, keys in merged_data.items()]

    # Sonucu JSON dosyasına yazma
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
    
# Oluşturmak istediğiniz klasörün yolu
directory = os.path.join(current_dir,"New Sheets")

# Klasörü oluşturma
if not os.path.exists(directory):
    os.makedirs(directory)

# Müzikleri doğru formata çevir
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

# Dosyayı daha okunabilir yap
file_list = os.listdir(os.path.join(current_dir, "New Sheets"))
for file in file_list:
    if file.endswith(".json"):
        normalizeJson(file)
        
        # clearing
        clr_list = os.listdir(os.path.join(current_dir, "New Sheets"))
        for i in clr_list:
            os.remove(os.path.join(current_dir, "New Sheets", i))

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
    ShowList()
    selection = int(input("Müziği seçin\n>> "))
    if selection > max(Sheet_dict) or selection <=0:
        print("Lütfen sadece listede olan sayılardan seçin")#çeviri ekle
        bring()
    else:
        selcted_music = Sheet_dict[selection]
bring()

filepath = os.path.join(current_dir, "Sheets", selcted_music + ".json")
df1 = pd.read_json(filepath)

def Timer(function="return-timer"):
    global salise
    global now
    global adjustment
    if function == "start":
        now = time.time()
        salise = int((now - int(now)) * 1000) 
        
    else:
        elapsed_time = time.time() - now 
        return salise + int(elapsed_time * 1000) 

SheetKeys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]
key = key[::-1]


def playMusic():
    countDown()
    global df1
    
    Timer("start") 
    for t in range(len(df1["time"])):
        note_time = df1["time"][t]
        current_time = Timer()  # wait timer
        
        while current_time < note_time:  # nota zamanı gelene kadar bekle
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
                    key_to_press = key[index]  # İlgili indeksteki tuşu belirle
                    notes_to_press.append(key_to_press)  # Basılacak notaları listeye ekle
                else:
                    print("geçersiz karakter:", char)
        # aynı anda Basılacak notaları aynı anda bas
        for key_to_press in notes_to_press:
            keyboard.press(key_to_press)
        print(notes_to_press)
        time.sleep(0.15)  # Küçük bir bekleme
        # Basılan notaları serbest bırak
        for key_to_press in notes_to_press:
            keyboard.release(key_to_press)

        if keyboard.is_pressed('"'):
            print(_("loop_ending"))
            break

playMusic()