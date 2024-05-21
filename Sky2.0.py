import time
import keyboard
import pandas as pd
import os
import json

current_dir = os.getcwd()

def normalizeJson(Fname):
    Fpath = os.path.join(current_dir, "New Sheets", Fname)
    print(Fpath)
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
            raise KeyError('Her item "time" ve "key" anahtarlarına sahip olmalıdır.')

    # Sonuçları birleştirilmiş formata çevirme
    result = [{'time': time, 'key': ','.join(keys)} for time, keys in merged_data.items()]

    # Sonucu JSON dosyasına yazma
    with open(os.path.join(current_dir, "Sheets", f'0{Fname}'), 'w', encoding="UTF-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    
def countDown():
    print("starting")
    time.sleep(1)
    print(4)
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)

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
    if selection > max(Sheet_dict):
        print("Lütfen sadece listede olan sayılardan seçin")
        bring()
    else:
        selcted_music = Sheet_dict[selection]
bring()

filepath = os.path.join(current_dir, "Sheets", selcted_music + ".json")
df1 = pd.read_json(filepath)

def Timer(function="return-time"):
    global salise
    global now
    global adjustment
    if function == "start":
        now = time.time()
        salise = int((now - int(now)) * 1000) 
        # adjustment = -2000  # -0.10 saniye başlangıç gecikmesi
    else:
        elapsed_time = time.time() - now 
        return salise + int(elapsed_time * 1000) 

SheetKeys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]
key = ["q", "w", "e", "r", "t", "a", "s", "d", "f", "g", "z", "x", "c", "v", "b",][::-1]#Sky Website
#key = ["y", "u", "ı", "o", "p", "h", "j", "k", "l", "ş", "n", "m", "ö", "ç", "b",][::-1]#TR keyboard
key =("y u ı o p h j k l ş n m ö ç b").split(" ")[::-1]
def playMusic():
    countDown()
    global df1
    Timer("start")  # Zamanı başlat
    
    for t in range(len(df1["time"])):
        note_time = df1["time"][t]
        current_time = Timer()  # Geçerli zamanı al
        
        while current_time < note_time:  # Zamanı bekleyerek, notanın zamanına kadar döngüde kal
            current_time = Timer()

        if keyboard.is_pressed('"'):
            print("loop_ending")
            break
        
        notes = df1["key"][t].split(",")  # Notaları virgülle ayırarak al
        notes_to_press = []  # Basılacak notaları bir listede topla
        for note in notes:
            pressed_keys = note.split(" ")  # Her nota içindeki karakterleri ayır
            for char in pressed_keys:
                char=char.replace("2Key","1Key").replace("3Key","1Key")
                char = char.strip()  # İşaretleri kaldır
                if char in SheetKeys:  # Eğer karakter SheetKeys içindeyse
                    index = SheetKeys.index(char)  # Karakterin indeksini al
                    key_to_press = key[index]  # İlgili indeksteki tuşu belirle
                    notes_to_press.append(key_to_press)  # Basılacak notaları listeye ekle
                else:
                    print("geçersiz karakter:", char)
        # Basılacak notaları aynı anda bas
        for key_to_press in notes_to_press:
            keyboard.press(key_to_press)
        print(notes_to_press)
        time.sleep(0.1)  # Küçük bir bekleme
        # Basılan notaları serbest bırak
        for key_to_press in notes_to_press:
            keyboard.release(key_to_press)

        if keyboard.is_pressed('"'):
            print("loop_ending")
            break

playMusic()
