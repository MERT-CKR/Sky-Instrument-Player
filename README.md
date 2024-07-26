Türkçe readme dosyası için [tıklayın](https://github.com/MERT-CKR/Sky-Instrument-Player/blob/main/README-TR.md)
---
## This application is designed to automatically play instruments in the game "Sky: Children of the Light" on the Steam platform.
## 👁 it on Youtube ↓
[![watch on YT](https://i3.ytimg.com/vi/ZUfYclM6AHA/maxresdefault.jpg)](https://www.youtube.com/watch?v=ZUfYclM6AHA)

### If you have downloaded the application, you can also test it on [Sky Music Nightly](https://specy.github.io/skyMusic/) without the game.

#### To run the program:
* Ensure that Python is installed on your computer.
### You need to install the following libraries:
* pandas
* keyboard

```cmd
pip install pandas
```

```cmd
pip install keyboard
```

### Usage:

When you first open the program, it will ask you to select a language.

## Depending on the environment where you will use the program, you need to select the key combination:

### 1. If you are using the instruments on the website, you can use the following key combination:
`
q w e r t a s d f g z x c v b
`

### 2. If you are using the instrument in the game:
When you equip the instrument in the game, enter the letters displayed on the buttons, separated by spaces. If there are dot or comma characters among them, change these to another key from Settings > Controls.

---

### Important Note

Select your music from the list and focus on the window where you will play the instrument. You need to be careful here; if you focus elsewhere, random keys will be pressed, which may trigger unwanted situations. For example, if you focus on a text document, it will type there. Therefore, make sure to keep the focus on the target window during the music playing process. To cancel the music playing process, press the `"` key several times consecutively.

---

### Adding other music to the list

Copy the music you want into the "SongDatabase" folder located in the same directory as "Sky-Auto Instrument Player.py" and paste them into the "New Sheets" folder. Restart or open the program.

If there is no folder named "New Sheets", it will be automatically created when you run the application.

It is not recommended to add too many files at once. Also, if the files you put in the "New Sheets" folder contain Japanese or other language characters, it may give an error. If you remove these characters and try again, it should work.

To change the language selection or key selection: run the reset key settings.py file.

The "Sheets" folder contains the music in the list. If you wish, you can rename them.
