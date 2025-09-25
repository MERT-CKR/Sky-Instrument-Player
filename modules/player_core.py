from modules.utils import *
from modules.utils import load_translations
_ = load_translations()
from keyboard import is_pressed, press_and_release
import keyboard


sheet_keys = ["1Key0","1Key1","1Key2","1Key3","1Key4","1Key5","1Key6","1Key7","1Key8","1Key9","1Key10","1Key11","1Key12","1Key13","1Key14"][::-1]


def while_speed_test():
    x = 0
    count = 0
    start = time.time()
    while time.time() - start < 1:
        x = 1
        count += 1
    print("1 saniyede:", count)



def playMusic(sheet, keybinds):
    print("benchmark test is running")
    while_speed_test()
    while_speed_test()
    while_speed_test()

    target = select_window()
    timer(1)
    t1 = time.time()
    counter = 0
    for line in sheet:
        key = line["key"]
        time1 = line["time"]#1 to avoid confusion with the library
        
        if key in sheet_keys:
            for i in range(len(sheet_keys)):
                key = key.replace(sheet_keys[i], keybinds[i])

        
        print(f"Time: {time1} Key {key.capitalize()}")
       
        
        current_time = timer() 
        while current_time < time1: # Wait for correct time
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
        
        keyboard.send(key)
        

    t2 = time.time()
    playtime = round(t2 - t1, 1)
    # print_yellow(_("sheet_type_note"))
    print(_("playback_duration").replace("*", str(playtime)))