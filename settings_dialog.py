import customtkinter as ctk
from PIL import Image
import datetime
import json
import os
import webbrowser
import threading
import requests
import sys
import keyboard

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  #type:ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

BG = "#0B0D14"
SIDEBAR = "#121526"
BUTTON_BASE = "#3B426A"
TEXT = "#E6E8EF"
HOVER_COLOR = "#1E2240"
SELECTED_COLOR = "#2A2F55"
ACCENT = "#6C7CFF"
SUCCESS = "#3FBAC2"
WARNING = "#FFB347"
DANGER = "#FF5555"

GITHUB_RAW_VERSION_URL = "https://raw.githubusercontent.com/MERT-CKR/Sky-AutoPlayer/main/settings.json"
GITHUB_REPO_URL = "https://github.com/MERT-CKR/Sky-AutoPlayer"
DISCORD_URL = "https://discord.gg/luvica0"
GITHUB_SPONSORS = "https://github.com/sponsors/MERT-CKR"

# 15 tuş layout
KEY_LAYOUT_15 = [
    ["key0", "key1", "key2", "key3", "key4"],
    ["key5", "key6", "key7", "key8", "key9"],
    ["key10", "key11", "key12", "key13", "key14"],
]

def load_settings(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["settings"][0] if "settings" in data else {}
    except Exception:
        return {}

def save_settings(path: str, updates: dict) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, val in updates.items():
            data["settings"][0][key] = val
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

class WindowPickerDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.on_select = on_select
        self.title("Select Game Window")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()
        try:
            self.after(200, lambda: self.iconphoto(True, parent.master._icon_ref))
        except:
            pass
        px = parent.winfo_x() + (parent.winfo_width() - 420) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 380) // 2
        self.geometry(f"420x380+{px}+{py}")
        ctk.CTkLabel(self, text="Select the game window:", font=ctk.CTkFont("Segoe UI", 13), text_color=TEXT).pack(pady=(20, 8))
        self.listbox = ctk.CTkScrollableFrame(self, fg_color=SIDEBAR, height=240)
        self.listbox.pack(fill="x", padx=20)
        self.selected_var = ctk.StringVar()
        self._load_windows()
        ctk.CTkButton(self, text="✓ Select", width=160, height=38, fg_color=ACCENT, hover_color="#5566dd",
                      text_color=TEXT, command=self._confirm).pack(pady=14)

    def _load_windows(self):
        try:
            import pygetwindow as gw
            windows = sorted([w.title for w in gw.getAllWindows() if w.title.strip()])
            for title in windows:
                row = ctk.CTkFrame(self.listbox, fg_color="transparent")
                row.pack(fill="x", pady=1)
                ctk.CTkRadioButton(row, text=title, variable=self.selected_var, value=title, text_color=TEXT,
                                   font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=10, pady=3)
        except Exception as e:
            ctk.CTkLabel(self.listbox, text=f"Error: {e}", text_color=DANGER).pack()

    def _confirm(self):
        val = self.selected_var.get()
        if val:
            self.on_select(val)
            self.destroy()

class ScanCodeDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_complete):
        super().__init__(parent)
        self.on_complete = on_complete
        self.scanned_keys = {}
        self.current_index = 0
        
        self.title("Scan Your Keyboard")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()
        
        px = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.geometry(f"500x400+{px}+{py}")
        
        ctk.CTkLabel(self, text="Setup Your Keyboard Layout", font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=TEXT).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Press each key on your keyboard when prompted.\nThe app will detect the key and scan code automatically.",
                     font=ctk.CTkFont("Segoe UI", 12), text_color="#8890aa", justify="center").pack(pady=(0, 20))
        
        self.progress_label = ctk.CTkLabel(self, text="Press key for position 0/15",
                                            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=ACCENT)
        self.progress_label.pack(pady=10)
        
        self.visual_grid = ctk.CTkFrame(self, fg_color=SIDEBAR, corner_radius=12)
        self.visual_grid.pack(padx=20, pady=20)
        
        self.key_labels = {}
        for r, row in enumerate(KEY_LAYOUT_15):
            for c, key_id in enumerate(row):
                lbl = ctk.CTkLabel(self.visual_grid, text="?", width=60, height=60, corner_radius=8,
                                   fg_color=BUTTON_BASE, text_color=TEXT, font=ctk.CTkFont("Segoe UI", 16, "bold"))
                lbl.grid(row=r, column=c, padx=5, pady=5)
                self.key_labels[key_id] = lbl
        
        self.status_label = ctk.CTkLabel(self, text="Waiting for key press...", font=ctk.CTkFont("Segoe UI", 11),
                                         text_color="#666a8a")
        self.status_label.pack(pady=10)
        
        self.bind("<KeyPress>", self._on_key_press)
        self.focus_set()

    def _on_key_press(self, event):
        if self.current_index >= 15:
            return
        
        char = event.char.lower()
        if not char or not char.isprintable() or len(char) != 1:
            self.status_label.configure(text="Invalid key! Press a single character key.", text_color=DANGER)
            return
        
        # Zaten kullanılmış mı kontrol et
        used_chars = [v["char"] for v in self.scanned_keys.values()]
        if char in used_chars:
            self.status_label.configure(text=f"Key '{char}' already used!", text_color=WARNING)
            return
        
        flat_keys = [k for row in KEY_LAYOUT_15 for k in row]
        key_id = flat_keys[self.current_index]
        
        # Hem char hem scan_code kaydet
        try:
            scan_code = keyboard.key_to_scan_codes(char)[0]
        except Exception:
            scan_code = None
        
        self.scanned_keys[key_id] = {"char": char, "scan_code": scan_code}
        self.key_labels[key_id].configure(text=char.upper(), fg_color=SUCCESS)
        
        self.current_index += 1
        
        if self.current_index >= 15:
            self.progress_label.configure(text="✓ Complete! Saving...", text_color=SUCCESS)
            self.status_label.configure(text="All keys scanned!", text_color=SUCCESS)
            self.after(1000, self._finish)
        else:
            self.progress_label.configure(text=f"Press key for position {self.current_index}/15")
            self.status_label.configure(text=f"Key '{char}' saved!", text_color=SUCCESS)

    def _finish(self):
        self.on_complete(self.scanned_keys)
        self.destroy()

class ProfileManagerDialog(ctk.CTkToplevel):
    def __init__(self, parent, settings_path, on_change):
        super().__init__(parent)
        self.settings_path = settings_path
        self.on_change = on_change
        self.settings = load_settings(settings_path)
        
        self.title("Manage Profiles")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()
        try:
            self.after(200, lambda: self.iconphoto(True, parent.master._icon_ref))
        except:
            pass
        
        px = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.geometry(f"500x450+{px}+{py}")
        
        ctk.CTkLabel(self, text="Keyboard Profiles", font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=TEXT).pack(pady=(20, 10))
        
        self.profiles = self.settings.get("profiles", {})
        self.active_profile = self.settings.get("active_profile", "Default")
        
        list_frame = ctk.CTkScrollableFrame(self, fg_color=SIDEBAR, height=250)
        list_frame.pack(fill="x", padx=20, pady=10)
        
        self.profile_vars = ctk.StringVar(value=self.active_profile)
        
        for name in self.profiles.keys():
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)
            
            radio = ctk.CTkRadioButton(row, text=name, variable=self.profile_vars, value=name,
                                        text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12))
            radio.pack(side="left", padx=10)
            
            if name != "Default":
                del_btn = ctk.CTkButton(row, text="🗑", width=30, height=30, fg_color=DANGER, hover_color="#cc4444",
                                        command=lambda n=name: self._delete_profile(n))
                del_btn.pack(side="right", padx=5)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="+ New Profile", width=140, height=38, fg_color=ACCENT, hover_color="#5566dd",
                      text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=self._create_profile).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="✓ Set Active", width=140, height=38, fg_color=SUCCESS, hover_color="#2F9BA8",
                      text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=self._set_active).pack(side="left", padx=5)
        
        self.status = ctk.CTkLabel(self, text="", font=ctk.CTkFont("Segoe UI", 11))
        self.status.pack()

    def _create_profile(self):
        dialog = ctk.CTkInputDialog(text="Enter profile name:", title="New Profile")
        name = dialog.get_input()
        if name and name not in self.profiles:
            def on_scan_complete(keys):
                self.profiles[name] = keys
                save_settings(self.settings_path, {"profiles": self.profiles})
                self.destroy()
                ProfileManagerDialog(self.master, self.settings_path, self.on_change)
            
            ScanCodeDialog(self, on_scan_complete)
        elif name:
            self.status.configure(text="Profile already exists!", text_color=WARNING)

    def _delete_profile(self, name):
        current_active = load_settings(self.settings_path).get("active_profile", "Default")
        
        if name == current_active:
            self.status.configure(text="Cannot delete active profile!", text_color=DANGER)
            return
        
        del self.profiles[name]
        save_settings(self.settings_path, {"profiles": self.profiles})
        self.destroy()
        ProfileManagerDialog(self.master, self.settings_path, self.on_change)

    def _set_active(self):
        selected = self.profile_vars.get()
        if selected and selected in self.profiles:
            save_settings(self.settings_path, {"active_profile": selected})
            self.status.configure(text=f"✓ Active profile: {selected}", text_color=SUCCESS)
            self.on_change()
            self.after(1000, self.destroy)

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, settings_path: str, on_profile_change=None):
        super().__init__(parent)
        self.settings_path = settings_path
        self.settings = load_settings(settings_path)
        self.on_profile_change = on_profile_change
        
        self.title("Settings")
        self.geometry("780x620")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()
        try:
            self.after(200, lambda: self.iconphoto(True, parent._icon_ref))
        except:
            pass
        
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() - 780) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 620) // 2
        self.geometry(f"780x620+{px}+{py}")
        
        self._build()
        self.bind("<Escape>", lambda e: self.destroy())

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=SIDEBAR, corner_radius=0, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="⚙  Settings", font=ctk.CTkFont("Segoe UI", 20, "bold"),
                     text_color=TEXT).pack(side="left", padx=24, pady=14)
        
        ver = self.settings.get("version", "?")
        ctk.CTkLabel(header, text=f"v{ver}", font=ctk.CTkFont("Segoe UI", 11), text_color="#555e8a",
                     fg_color=HOVER_COLOR, corner_radius=8, padx=10, pady=4).pack(side="right", padx=20)
        
        self.tabview = ctk.CTkTabview(self, fg_color=BG, segmented_button_fg_color=SIDEBAR,
                                       segmented_button_selected_color=ACCENT, segmented_button_selected_hover_color="#5566dd",
                                       segmented_button_unselected_color=SIDEBAR, segmented_button_unselected_hover_color=HOVER_COLOR,
                                       text_color=TEXT)
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(8, 0))
        
        self.tabview.add("⌨️  Profiles")
        self.tabview.add("🌐  About")
        self.tabview.add("🔄  Updates")
        
        self._build_profiles(self.tabview.tab("⌨️  Profiles"))
        self._build_about(self.tabview.tab("🌐  About"))
        self._build_updates(self.tabview.tab("🔄  Updates"))

    def _build_profiles(self, tab):
        ctk.CTkLabel(tab, text="Manage your keyboard layouts and switch between profiles.",
                     font=ctk.CTkFont("Segoe UI", 12), text_color="#888fa8").pack(pady=(10, 20))
        
        active = self.settings.get("active_profile", "Default")
        ctk.CTkLabel(tab, text=f"Active Profile: {active}", font=ctk.CTkFont("Segoe UI", 14, "bold"),
                     text_color=ACCENT).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="📋  Manage Profiles", width=200, height=45, fg_color=ACCENT, hover_color="#5566dd",
                      text_color=TEXT, font=ctk.CTkFont("Segoe UI", 13, "bold"),
                      command=self._open_profile_manager).pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="🎮  Select Game Window", width=200, height=40, fg_color=HOVER_COLOR,
                      hover_color=SELECTED_COLOR, text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12),
                      command=self._open_window_picker).pack(pady=5)
        
        ctk.CTkButton(btn_frame, text="📂  Open Sheets Folder", width=200, height=40, fg_color=HOVER_COLOR,
                      hover_color=SELECTED_COLOR, text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12),
                      command=self._open_sheets_dir).pack(pady=5)
        
        self._window_label = ctk.CTkLabel(tab, text=f"Target: {self.settings.get('target_window', 'Not set')}",
                                          font=ctk.CTkFont("Segoe UI", 11), text_color="#666a8a")
        self._window_label.pack(pady=10)
        
        self._status = ctk.CTkLabel(tab, text="", font=ctk.CTkFont("Segoe UI", 12))
        self._status.pack()

    def _open_profile_manager(self):
        ProfileManagerDialog(self, self.settings_path, self._on_profile_changed)

    def _on_profile_changed(self):
        self.settings = load_settings(self.settings_path)
        if self.on_profile_change:
            self.on_profile_change()
        self._status.configure(text="✓ Profile changed! Buttons updated.", text_color=SUCCESS)
        self.after(3000, lambda: self._status.configure(text=""))

    def _open_window_picker(self):
        def on_select(title):
            save_settings(self.settings_path, {"target_window": title})
            self.settings["target_window"] = title
            self._window_label.configure(text=f"Target: {title}")
        WindowPickerDialog(self, on_select)

    def _open_sheets_dir(self):
        import subprocess
        sheets_dir = os.path.join(os.path.dirname(self.settings_path), "sheets")
        try:
            os.makedirs(sheets_dir, exist_ok=True)
            subprocess.Popen(f'explorer.exe "{sheets_dir}"')
            self._status.configure(text="✓ Opened in Explorer", text_color=SUCCESS)
        except Exception as e:
            self._status.configure(text=f"❌ Error: {str(e)[:30]}", text_color=DANGER)
        self.after(3000, lambda: self._status.configure(text=""))

    def _build_about(self, tab):
        def load_icon(filename, size=(56, 56)):
            try:
                from customtkinter import CTkImage
                return CTkImage(Image.open(resource_path(f"assets/{filename}")), size=size)
            except Exception:
                return None
        
        gh_img = load_icon("github.png")
        dc_img = load_icon("discord.png", size=(66, 56))
        sponsors_img = load_icon("sponsors.png", size=(66, 66))
        
        ctk.CTkLabel(tab, text="Sky Auto Instrument Player", font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=TEXT).pack(pady=(18, 2))
        
        ver = self.settings.get("version", "?")
        ctk.CTkLabel(tab, text=f"Version {ver}", font=ctk.CTkFont("Segoe UI", 12), text_color="#666a8a").pack(pady=(0, 14))
        
        ctk.CTkLabel(tab, text="An open-source auto-player for Sky: Children of the Light's instruments.\nSelect a sheet, configure your keyboard, and let it play.",
                     font=ctk.CTkFont("Segoe UI", 12), text_color="#8890aa", justify="center").pack(pady=(0, 18))
        
        links_frame = ctk.CTkFrame(tab, fg_color="transparent")
        links_frame.pack()
        
        links = [
            {"icon": "⌥", "img": gh_img, "label": "Source Code", "sub": "GitHub repository", "url": GITHUB_REPO_URL},
            {"icon": "◈", "img": dc_img, "label": "Discord", "sub": "Ask Developer", "url": DISCORD_URL},
            {"icon": "☕", "img": sponsors_img, "label": "Sponsors", "sub": "Support the project", "url": GITHUB_SPONSORS},
        ]
        
        for link in links:
            card = ctk.CTkFrame(links_frame, fg_color=SIDEBAR, corner_radius=14, width=200, height=140)
            card.pack(side="left", padx=10, pady=6)
            card.pack_propagate(False)
            
            if link["img"]:
                ctk.CTkLabel(card, image=link["img"], text="").place(relx=0.5, y=20, anchor="n")
            else:
                ctk.CTkLabel(card, text=link["icon"], font=ctk.CTkFont("Segoe UI", 36), text_color=ACCENT).place(relx=0.5, y=20, anchor="n")
            
            ctk.CTkLabel(card, text=link["label"], font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=TEXT).place(relx=0.5, y=86, anchor="n")
            ctk.CTkLabel(card, text=link["sub"], font=ctk.CTkFont("Segoe UI", 10), text_color="#666a8a").place(relx=0.5, y=110, anchor="n")
            
            for widget in card.winfo_children():
                widget.bind("<Button-1>", lambda e, u=link["url"]: webbrowser.open(u))
            card.bind("<Button-1>", lambda e, u=link["url"]: webbrowser.open(u))
            card.configure(cursor="hand2")
        
        copyright_container = ctk.CTkFrame(tab, fg_color="transparent")
        copyright_container.pack(side="bottom", fill="x", pady=(0, 20))
        
        ctk.CTkFrame(copyright_container, fg_color="#2a2f4a", height=1).pack(fill="x", padx=60, pady=(0, 12))
        ctk.CTkLabel(copyright_container, text="Made with 🤍 by Mert Çakır", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color="#6a7090").pack()
        
        current_year = datetime.datetime.now().year
        license_label = ctk.CTkLabel(copyright_container, text=f"© {current_year} • Apache License 2.0",
                                      font=ctk.CTkFont("Segoe UI", 9), text_color="#5a7090", cursor="hand2")
        license_label.pack(pady=(3, 0))
        license_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.apache.org/licenses/LICENSE-2.0"))

    def _build_updates(self, tab):
        self._update_status_label = ctk.CTkLabel(tab, text="Check if a new version is available on GitHub.",
                                                  font=ctk.CTkFont("Segoe UI", 13), text_color="#8890aa")
        self._update_status_label.pack(pady=(40, 16))
        
        self._update_detail = ctk.CTkLabel(tab, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=TEXT,
                                           wraplength=480, justify="center")
        self._update_detail.pack(pady=(0, 20))
        
        self._check_btn = ctk.CTkButton(tab, text="🔍  Check for Updates", width=200, height=42, fg_color=ACCENT,
                                         hover_color="#5566dd", text_color=TEXT, font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                         command=self._check_updates)
        self._check_btn.pack()
        
        ctk.CTkButton(tab, text="⌥  Open GitHub Releases", width=200, height=38, fg_color=HOVER_COLOR,
                      hover_color=SELECTED_COLOR, text_color=TEXT, font=ctk.CTkFont("Segoe UI", 12),
                      command=lambda: webbrowser.open(GITHUB_REPO_URL + "/releases")).pack(pady=(10, 0))
        
        ver = self.settings.get("version", "?")
        ctk.CTkLabel(tab, text=f"Current version: v{ver}", font=ctk.CTkFont("Segoe UI", 11),
                     text_color="#444a6a").pack(pady=(30, 0))

    def _check_updates(self):
        if not HAS_REQUESTS:
            self._update_status_label.configure(text="⚠  'requests' module not installed.", text_color=WARNING)
            return
        self._check_btn.configure(text="⏳  Checking...", state="disabled")
        self._update_status_label.configure(text="Fetching version from GitHub...", text_color="#8890aa")
        self._update_detail.configure(text="")
        threading.Thread(target=self._fetch_version, daemon=True).start()

    def _fetch_version(self):
        try:
            r = requests.get(GITHUB_RAW_VERSION_URL, timeout=5)
            r.raise_for_status()
            data = r.json()
            remote = data["settings"][0]["version"]
            local = self.settings.get("version", "0")
            
            if remote > local:
                self.after(0, lambda: self._show_update_result(f"🎉  New version available: v{remote}", SUCCESS, True))
            else:
                self.after(0, lambda: self._show_update_result(f"✓  You're up to date! (v{local})", SUCCESS, False))
        except Exception as e:
            self.after(0, lambda: self._show_update_result(f"❌  Could not reach GitHub: {str(e)[:60]}", DANGER, False))
        finally:
            self.after(0, lambda: self._check_btn.configure(text="🔍  Check for Updates", state="normal"))

    def _show_update_result(self, msg, color, show_open):
        self._update_status_label.configure(text=msg, text_color=color)
        if show_open:
            self._update_detail.configure(text="Click 'Open GitHub Releases' below to download the latest version.",
                                          text_color="#8890aa")