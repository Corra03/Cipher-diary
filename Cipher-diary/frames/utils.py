import tkinter as tk
from tkinter import ttk


def add_back_button(self):
    btn = ttk.Button(self, text="← Back",
                     command=lambda: self.master.show_frame("menu"))
    btn.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


def create_password_form(parent, row_start=0, with_confirmation=False):
    label = ttk.Label(parent, text="Inserisci la password")
    label.grid(row=row_start, column=0, pady=5)

    entry = ttk.Entry(parent, show="*")
    entry.grid(row=row_start + 1, column=0, padx=40, pady=5)

    entry_confirm = None

    if with_confirmation:
        label2 = ttk.Label(parent, text="Conferma la password")
        label2.grid(row=row_start + 2, column=0, pady=(5, 0))

        entry_confirm = ttk.Entry(parent, show="*")
        entry_confirm.grid(row=row_start + 3, column=0, padx=40, pady=5)

    return entry, entry_confirm

def confirmation_btn(parent, command):
    btn = ttk.Button(
        parent,
        text="Conferma",
        command=command
    )
    btn.grid(row=6, column=0, padx=20, pady=15)
    return btn
