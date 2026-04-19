import tkinter as tk
from tkinter import ttk
root = tk.Tk()


root.title("Cipher-diary")


def psw():
    label = tk.Label(root, text="Inserire la password")
    entry = tk.Entry(root)
    psw = entry.get()
    label.pack()
    entry.pack()

def new():
    print("Hai cliccato!")

def read():
    print("dedneik")


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)

new_b = ttk.Button(root, text="New", command=new)
read_b = ttk.Button(root, text="Read", command=read)
new_b.grid(row = 2, column = 0,sticky="nsew",   padx=10, ipadx=20, ipady=10, pady=40)
read_b.grid(row = 2, column = 2,sticky="nsew",   padx=10, ipadx=20, ipady=10, pady=40)

root.geometry("300x200")

root.mainloop()