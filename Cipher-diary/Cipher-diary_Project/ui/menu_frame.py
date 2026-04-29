# frames/menu_frame.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()
    def go_to_read(self):
        self.master.show_frame("read")

    '''        def read_action():
                file_path = filedialog.askopenfilename(
                    title="Seleziona un file",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )

                return file_path

            file_path = read_action()
            if file_path:
                read_frame = self.master._frames["read"]
                read_frame.set_file(file_path)
                self.master.show_frame("read")'''

    def _build_ui(self):




        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        label = ttk.Label(self, text="Cipher-diary")
        label.grid(row=0, column=0, sticky="n", pady=20)

        btn_new = ttk.Button(self, text="New",
                             command=lambda: self.master.show_frame("new"))
        btn_new.grid(row=1, column=0, sticky="nsew", padx=40, pady=10)

        btn_read = ttk.Button(self, text="Read",
                              command=self.go_to_read )
        btn_read.grid(row=2, column=0, sticky="nsew", padx=40, pady=10)
