# frames/menu_frame.py
import tkinter as tk
from tkinter import ttk
from . import utils as ut
class NewFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Titolo pagina
        label_new = ttk.Label(
            self,
            text="NUOVA PAGINA"
        )
        label_new.grid(row=1, column=0, pady=5, sticky="n")

        ut.add_back_button(self)
        entry_psw, entry_confirm = ut.create_password_form(self, row_start=2, with_confirmation=True)

        def confirm_psw():
            psw1 = entry_psw.get()

            if entry_confirm:
                psw2 = entry_confirm.get()
                if psw1 == psw2 and psw1 != "":
                    print("Password corretta")
                else:
                    print("Le password non coincidono")
            else:
                if psw1 != "":
                    print("Password inserita:", psw1)
                else:
                    print("Password vuota")

            # Bottone conferma

        ut.confirmation_btn(self, command=confirm_psw)

