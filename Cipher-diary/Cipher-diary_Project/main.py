# main.py
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from core.config import CONFIG_DIR, CONFIG_FILE, init_config
from ui.ask_diary_folder import _ask_diary_folder

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cipher-diary")
        self.geometry("450x400")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._frames = {}
        self._load_frames()
        self.show_frame("menu")

    def _load_frames(self):
        for name, FrameClass in [("menu", MenuFrame),
                                  ("new", NewFrame),
                                  ("read", ReadFrame),
                                  ("options", Options)]:

            frame = FrameClass(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self._frames[name] = frame

    def show_frame(self, name):
        if name == "read":
            path = filedialog.askopenfilename(
                filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
            )
            if not path:
                return
            self._frames["read"].set_path(path)
        self._frames[name].tkraise()


if __name__ == "__main__":
    config_path = CONFIG_DIR / CONFIG_FILE
    first_run = not config_path.exists()
    cfg = init_config()
    if first_run:
        _ask_diary_folder(cfg)
    from ui.menu_frame import MenuFrame
    from ui.new_frame import NewFrame
    from ui.read_frame import ReadFrame
    from ui.options import Options
    app = App()
    app.mainloop()