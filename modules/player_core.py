from utils import *
from utils import load_translations
_ = load_translations()
from keyboard import press, is_pressed, press_and_release

keybinds= ""

#ascii desteği

def playMusic(sheet, sheet_keys):
    select_window()
   
    timer(1)

    for line in sheet:
        key = line["key"]
        time1 = line["time"]#1 to avoid confusion with the library
        
        if key in sheet_keys:
            for i in range(len(sheet_keys)):
                key = key.replace(sheet_keys[i], keybinds[i])

        
        print(f"Time {time1} - Key {key}")
        counter = 0
        current_time = timer()
        while current_time < time1: # Wait for correct time
            current_time = timer()
            # time.sleep(0.0005)
            # time.sleep(0.08)
            current_time = timer()
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
