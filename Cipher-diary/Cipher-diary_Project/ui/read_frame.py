# ui/read_frame.py
import tkinter as tk
from tkinter import messagebox
from app.Editor_window import EditorApp
from core.crypto import decrypt
from . import utils as ut


class ReadFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._path = None
        self._build_ui()

    def set_path(self, path: str):
        self._path = path

    def _build_ui(self):
        def confirm_psw():
            psw = entry_psw.get()
            try:
                with open(self._path, "rb") as fh:
                    decrypt(fh.read(), psw)
            except Exception:
                messagebox.showerror("Errore", "Password errata o file non valido.")
                return

            self.winfo_toplevel().destroy()
            EditorApp(path=self._path, psw=psw).mainloop()

        ut.add_back_button(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        tk.Label(self, text="LETTURA").grid(row=1, column=0, sticky="n")

        entry_psw = ut.create_password_form(self, row_start=2, with_confirmation=False)

        ut.confirmation_btn(self, command=confirm_psw)




'''    def _build_ui(self):
        def confirm_psw():
            result = True

            if result:
                self.winfo_toplevel().destroy()
                app = EditorApp(path= )
                app.mainloop()

        ut.add_back_button(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)


        label_read = tk.Label(self, text="LETTURA")
        label_read.grid(row=1, column=0, sticky="n")

        entry_psw = ut.create_password_form(self, row_start=2)


        ut.confirmation_btn(self, command=confirm_psw)'''



'''
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
        self.text.insert(tk.END, content)'''