# module: get_scan_code
import os
import json
import keyboard


from modules.utils import print_green, print_red,print_yellow
from modules.utils import load_translations
_ = load_translations()





class get_layout:
    def __init__(self, layout_name):
        self.key_dict = {}
        self.ln = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.empty_list = self.ln.copy()
        self.text= f"     Your {layout_name.replace("_"," ")}"
        self.border = "  ---------------------------"
        self.layout_name = layout_name
        self.run()


    def print_layout(self):
        self.clear_console()
        print_green
        layout1=      f"|  {self.ln[0]}  |  {self.ln[1]}  |  {self.ln[2]}  |  {self.ln[3]}  |  {self.ln[4]}  |"
        layout2=      f"|  {self.ln[5]}  |  {self.ln[6]}  |  {self.ln[7]}  |  {self.ln[8]}  |  {self.ln[9]}  |"
        layout3=    f"|  {self.ln[10]}  |  {self.ln[11]}  |  {self.ln[12]}  |  {self.ln[13]}  |  {self.ln[14]}  |"

        print_yellow(_("add_sky_layout"))

        print_green(self.text)

        print_red(self.border)
        print(layout1)

        print_red(self.border)
        print(layout2)

        print_red(self.border)
        print(layout3)

        print_red(self.border)
        print("\n\n\n")



    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def key_scan_code(self):
        self.print_layout()

        for i in range(15):
            print_green(_("instrument_layout"))
            event = keyboard.read_event()
            while event.event_type != keyboard.KEY_DOWN:
                event = keyboard.read_event()

            if len(event.name) > 1:
                raise ValueError(_("invalid_char"))
            

            if event.name not in self.ln:
                self.ln[i] = event.name
                self.print_layout()
            else:
                KeyError(_("repeat_error"))
                
            
            self.key_dict[event.name] = event.scan_code
            print(f"{len(self.key_dict)}/15")

        if len(self.key_dict) != 15:
            raise IndexError(_("length_error"))
            
    def save(self):
        
        with open("modules\\key_layouts.json", "r", encoding="utf-8") as file:
            key_layouts = json.load(file)


        key_layouts["layouts"][0][self.layout_name] = self.key_dict


        with open("modules\\key_layouts.json", "w", encoding="utf-8") as file:
            json.dump(key_layouts, file, indent=4, ensure_ascii=False)

        print_green(_("layouts_updated"))
        print_green(_("press_enter"))
        input(">> ")

    def run(self):
        self.print_layout()
        self.key_scan_code()
        print(self.key_dict)
        self.save()
        return self.key_dict


