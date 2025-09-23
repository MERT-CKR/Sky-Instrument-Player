from modules.utils import *
from modules.utils import load_translations
_ = load_translations()
from keyboard import press, is_pressed, press_and_release


sheet_keys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]

def playMusic(sheet, keybinds):
    target = select_window()
    timer(1)

    for line in sheet:
        key = line["key"]
        time1 = line["time"]#1 to avoid confusion with the library
        
        if key in sheet_keys:
            for i in range(len(sheet_keys)):
                key = key.replace(sheet_keys[i], keybinds[i])

        
        print(f"Time: {time1} Key {key.capitalize()}")
        
        counter = 0
        current_time = timer()
        while current_time < time1: # Wait for correct time
            current_time = timer()
            counter +=1
            print(counter)
            if counter%200 == 0:
                print("\n")

        
        if is_pressed('"'):
            break

        if target != None:
            if gw.getActiveWindowTitle() != target:
                print(_("focus_lost"))
                break
        
        press_and_release(key)
        
        # release(key)
