# frames/menu_frame.py
import tkinter as tk
from tkinter import ttk

from . import utils as ut

class ReadFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):


        ut.add_back_button(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)


        label_read = tk.Label(self, text="LETTURA")
        label_read.grid(row=1, column=0, sticky="n")

        self.text = tk.Text(self)
        self.text.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)


    def set_file(self, path):
        self.file_path = path
        entry_psw = ut.create_password_form(self, row_start=2)
        def confirm_psw():
            #qui dovresti provare a decriptsre il file con try chatch
            return True

        ut.confirmation_btn(self, command=confirm_psw)
        with open(path, "r") as f:
            content = f.read()


        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)