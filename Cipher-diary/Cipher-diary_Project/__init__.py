# main.py
import tkinter as tk
from ui.menu_frame import MenuFrame
from ui.new_frame import NewFrame
from ui.read_frame import ReadFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cipher-diary")
        self.geometry("400x250")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._frames = {}
        self._load_frames()
        self.show_frame("menu")

    def _load_frames(self):
        for name, FrameClass in [("menu", MenuFrame),
                                  ("new", NewFrame),
                                  ("read", ReadFrame)]:

            frame = FrameClass(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self._frames[name] = frame

    def show_frame(self, name):
        self._frames[name].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()