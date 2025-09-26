from modules.utils import *
from modules.utils import load_translations
_ = load_translations()
from keyboard import is_pressed, press_and_release
import keyboard
import threading

# sheet_keys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]

key_dict = {
    "1Key0": [],
    "1Key1": [],
    "1Key2": [],
    "1Key3": [],
    "1Key4": [],
    "1Key5": [],
    "1Key6": [],
    "1Key7": [],
    "1Key8": [],
    "1Key9": [],
    "1Key10": [],
    "1Key11": [],
    "1Key12": [],
    "1Key13": [],
    "1Key14": []
}
key_dict_keys = list(key_dict.keys())


def delayed_release(key, delay=0.05):
    """Tuşu delay kadar basılı tutup bırakır (thread içinde çalışır)."""
    time.sleep(delay)
    keyboard.release(key)

def playMusic(sheet, key_layout):
    count = 0

    for key, value in key_layout.items():
        key_dict[key_dict_keys[count]] = [key, value]
        count+=1
    print(key_dict)

    target = select_window()
    timer(1)
    t1 = time.time()
    counter = 0
    for line in sheet:
        key = line["key"]
        time1 = line["time"]#1 to avoid confusion with the library
        
        if key in key_dict_keys:
            keyboard_key = key_dict[key][0]
            scan_code = key_dict[key][1]

        else:
            print_red("unknown key !!!:", key)

        
        print(f"Time: {time1}  Key: {keyboard_key.capitalize()}")
       
        
        current_time = timer() 
        while current_time < time1+250: # Wait for correct time
            current_time = timer()
            counter +=1
            time.sleep(0.0005)
            
            if counter%150 == 0:
                print("\n")

        
        if is_pressed('"'):
            break

        if target != None:
            if gw.getActiveWindowTitle() != target:
                print(_("focus_lost"))
                break
        
        keyboard.press(scan_code)
        threading.Thread(target=delayed_release, args=(scan_code, 0.07), daemon=True).start()
        

        

    t2 = time.time()
    playtime = round(t2 - t1, 1)
    # print_yellow(_("sheet_type_note"))
    print(_("playback_duration").replace("*", str(playtime)))