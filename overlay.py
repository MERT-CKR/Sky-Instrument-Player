import tkinter as tk
import queue
from PIL import Image, ImageDraw, ImageTk

KEY_LAYOUT = [
    ["key0",  "key1",  "key2",  "key3",  "key4"],
    ["key5",  "key6",  "key7",  "key8",  "key9"],
    ["key10", "key11", "key12", "key13", "key14"],
]

CELL_W = 48
CELL_H = 36
GAP = 6
PAD = 14
COLS = 5
ROWS = 3

PANEL_W = COLS * CELL_W + (COLS - 1) * GAP + PAD * 2
PANEL_H = ROWS * CELL_H + (ROWS - 1) * GAP + PAD * 2

BG_COLOR   = "#282d46"
KEY_NORMAL = "#bec8ff"
KEY_ACTIVE = "#6C7CFF"
TEXT_COLOR = "#101020"


CORNER_RADIUS = 12
WINDOW_RADIUS = 16


class Overlay(tk.Tk):
    def __init__(self, profile: dict):
        super().__init__()
        self._profile = profile
        self._cells = {}
        self._anim_jobs = {}
        self._trigger_queue = queue.Queue()

        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-alpha", 0.82)
        self.configure(bg=BG_COLOR)

        self._apply_window_mask()

        self.canvas = tk.Canvas(
            self, width=PANEL_W, height=PANEL_H,
            bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.pack()

        for r, row in enumerate(KEY_LAYOUT):
            for c, key_id in enumerate(row):
                x1 = PAD + c * (CELL_W + GAP)
                y1 = PAD + r * (CELL_H + GAP)
                x2 = x1 + CELL_W
                y2 = y1 + CELL_H
                rx = (x1 + x2) // 2
                ry = (y1 + y2) // 2
                char = profile.get(key_id, "?")
                
                rect = self._create_rounded_rect(x1, y1, x2, y2, 
                                                  radius=CORNER_RADIUS, 
                                                  fill=KEY_NORMAL)
                
                text = self.canvas.create_text(rx, ry, text=char.upper(),
                                               fill=TEXT_COLOR,
                                               font=("Segoe UI", 11, "bold"))
                self._cells[key_id] = (rect, text)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = sw - PANEL_W - 36
        y = sh - PANEL_H - 60
        self.geometry(f"{PANEL_W}x{PANEL_H}+{x}+{y}")

        self._process_triggers()

    def _apply_window_mask(self):
        try:
            if hasattr(self, 'wm_attributes'):
                self.update_idletasks()
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                    
                    DWMWA_WINDOW_CORNER_PREFERENCE = 33
                    DWMWCP_ROUND = 2
                    
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd,
                        DWMWA_WINDOW_CORNER_PREFERENCE,
                        ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                        ctypes.sizeof(ctypes.c_int)
                    )
                except Exception:
                    self.after(100, self._apply_pill_mask)
        except Exception as e:
            print(f"Window mask error: {e}")

    def _apply_pill_mask(self):
        try:
            mask = Image.new('L', (PANEL_W, PANEL_H), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle(
                [(0, 0), (PANEL_W, PANEL_H)],
                radius=WINDOW_RADIUS,
                fill=255
            )
            
            self.wm_attributes("-transparentcolor", "white")
            
        except Exception as e:
            print(f"PIL mask error: {e}")

    def _create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Yuvarlak köşeli dikdörtgen çiz (smooth polygon)"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _process_triggers(self):
        try:
            while not self._trigger_queue.empty():
                key_id = self._trigger_queue.get_nowait()
                self._do_trigger(key_id)
        except Exception:
            pass
        self.after(16, self._process_triggers)

    def trigger(self, key_id: str):
        self._trigger_queue.put(key_id)

    def _do_trigger(self, key_id: str):
        if key_id not in self._cells:
            return
        rect, _ = self._cells[key_id]
        self.canvas.itemconfig(rect, fill=KEY_ACTIVE)
        if key_id in self._anim_jobs:
            try:
                self.after_cancel(self._anim_jobs[key_id])
            except Exception:
                pass
        self._anim_jobs[key_id] = self.after(180, lambda k=key_id: self._reset(k))

    def _reset(self, key_id: str):
        if key_id in self._cells:
            rect, _ = self._cells[key_id]
            self.canvas.itemconfig(rect, fill=KEY_NORMAL)
        self._anim_jobs.pop(key_id, None)

    def update_profile(self, profile: dict):
        self._profile = profile
        for key_id, (_, text_id) in self._cells.items():
            char = profile.get(key_id, "?")
            self.canvas.itemconfig(text_id, text=char.upper())