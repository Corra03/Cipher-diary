# frames/menu_frame.py
import tkinter as tk
from tkinter import ttk
from . import utils as ut
from app.Editor_window import EditorApp
class NewFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)

        ut.add_back_button(self)

        center = ttk.Frame(self)
        center.grid(row=2, column=0)
        center.columnconfigure(0, weight=1)



        ttk.Label(center, text="Nuova pagina",
                  font=("Segoe UI", 11)).grid(
                  row=0, column=0, pady=(0, 20))

        entry_psw, entry_confirm = ut.create_password_form(
            center, row_start=1, with_confirmation=True)

        def confirm_psw():
            psw1 = entry_psw.get()
            if entry_confirm:
                psw2 = entry_confirm.get()
                if psw1 == psw2 and psw1 != "":
                    self.winfo_toplevel().destroy()
                    app = EditorApp(psw1)
                    app.mainloop()
                else:
                    print("Le password non coincidono")
            else:
                if psw1 != "":
                    print("Password inserita:", psw1)

        ut.add_back_button(self)
        ut.confirmation_btn(center, command=confirm_psw)
