#### Other Languages: [Türkçe](https://github.com/MERT-CKR/Sky-Instrument-Player/blob/main/README-TR.md)

---
## This application is designed to automatically play instruments in the game "Sky: Children of the Light" on the Steam platform.

## 👁 it on Youtube ↓
[![watch on YT](https://i3.ytimg.com/vi/ZUfYclM6AHA/maxresdefault.jpg)](https://www.youtube.com/watch?v=ZUfYclM6AHA)



#### To run the program:
* Ensure that [Python](https://www.python.org) is installed on your computer.
#### You need to install the following libraries:
* pandas
* keyboard
* requests

paste the fallowing codes to your terminal (CMD)

```cmd
pip install pandas
```

```cmd
pip install keyboard
```

```cmd
pip install requests
```

## Usage:

When you first open the program, it will ask you to select a language.

Only English and Turkish languages supported

### Depending on the environment where you will use the program, you need to select the key combination:

#### 1. If you are using the instruments on the `Sky Music Nightly`, you can use the following key combination:
`
q w e r t a s d f g z x c v b
`

#### 2. If you are using the instrument in the game:
* When you equip the instrument in the game, enter the letters displayed on the buttons, separated by spaces. 

* If there are dot or comma characters among them, change these to another key from Settings > Controls.



#### If you have downloaded the application, you can also test it on [Sky Music Nightly](https://specy.github.io/skyMusic/) without the game.


---

> [!IMPORTANT]
> Select your music from the list and focus on the window where you will play the instrument. You need to be careful here; if you focus elsewhere, random keys will be pressed, which may trigger unwanted situations.
For example, if you focus on a text document, it will type there. Therefore, make sure to keep the focus on the target window during the music playing process. To cancel the music playing process, press and hold the `"` key untill music stop.

---
### To change the language selection or key selection:
* Run the `reset key settings.py` file.

## How to add other sheet musics to the list?

* ### If you already have sheets 
    * Just copy them `New Sheets` folder
    * Ensure your file includes only 1 layer to play


* ### If you don't have sheets
    * Copy the sheets you want into the `SongDatabase` folder located in the same directory as `Sky-Auto Instrument Player.py` and paste them into the `New Sheets` folder. Then Restart or open the program.

* ### Supported Sheet formats
    * `.txt`
    * `.json`
    * `.skysheet`
    


* If you copy your Sheets into `New Sheets` folder and you can't find Original files. Then you can find them at the folder named `Raw Sheets`

* If there is no folder named `New Sheets` or `Raw Sheets` it will be automatically created when you run the application.

* It is not recommended to add too many files at once. Also, if the files you put in the `New Sheets` folder contain Japanese or other language characters, it may give an error. If you remove these characters and try again, it should work.


* The `Sheets` folder contains the music in the list. If you wish, you can rename or remove them.


---
### Didn't you find what you were looking for?
* working on a Wiki For `Auto-Instrument Player`
* Reach me on Discord: luvica0


