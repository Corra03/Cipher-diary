import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.title("Cipher-diary")
root.geometry("400x250")

# -------------------
# ROOT RESPONSIVE
# -------------------
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# -------------------
# CONTENITORE PAGINE
# -------------------
container = tk.Frame(root)
container.grid(row=0, column=0, sticky="nsew")

# -------------------
# FUNZIONE CAMBIO PAGINA
# -------------------
def show_frame(frame):
    frame.tkraise()

# ===================
# FRAME MENU
# ===================
menu_frame = tk.Frame(container)
menu_frame.grid(row=0, column=0, sticky="nsew")

menu_frame.columnconfigure(0, weight=1)
menu_frame.rowconfigure((0,1,2,3), weight=1)

label_menu = tk.Label(menu_frame, text="MENU")
label_menu.grid(row=0, column=0, sticky="nsew")

btn_new = ttk.Button(menu_frame, text="New",
                     command=lambda: show_frame(new_frame))
btn_read = ttk.Button(menu_frame, text="Read",
                      command=lambda: show_frame(read_frame))

btn_new.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
btn_read.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

# ===================
# FRAME NEW
# ===================
new_frame = tk.Frame(container)
new_frame.grid(row=0, column=0, sticky="nsew")

new_frame.columnconfigure(0, weight=1)
new_frame.rowconfigure((0,1,2,3,4), weight=1)

# BACK in alto a sinistra
btn_back1 = ttk.Button(
    new_frame,
    text="← Back",
    command=lambda: show_frame(menu_frame)
)
btn_back1.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# Titolo pagina
label_new = ttk.Label(
    new_frame,
    text="NUOVA PAGINA"
)
label_new.grid(row=1, column=0, pady=5, sticky="n")

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


entry_psw, entry_confirm = create_password_form(new_frame, row_start=2, with_confirmation=True)
def confirm_psw():
    print("NDjsns")
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
btn_confirm = ttk.Button(
        new_frame,
        text="Conferma",
        command=confirm_psw
    )
btn_confirm.grid(row=6, column=0, padx=20, pady=15)



# ===================
# FRAME READ
# ===================
read_frame = tk.Frame(container)
read_frame.grid(row=0, column=0, sticky="nsew")

read_frame.columnconfigure(0, weight=1)
read_frame.rowconfigure((0,1,2,3), weight=1)

# BACK in alto a sinistra
btn_back2 = ttk.Button(read_frame, text="← Back",
                       command=lambda: show_frame(menu_frame))
btn_back2.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

label_read = tk.Label(read_frame, text="LETTURA")
label_read.grid(row=1, column=0, sticky="n")

def read_action():
    print("dedneik")

btn_read_action = ttk.Button(read_frame, text="Leggi",
                             command=read_action)
btn_read_action.grid(row=2, column=0, sticky="n", padx=20, pady=10)

# -------------------
# STACK FRAME
# -------------------
for frame in (menu_frame, new_frame, read_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# pagina iniziale



show_frame(menu_frame)

root.mainloop()