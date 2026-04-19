import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font

class EditorWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Editor Test")
        self.geometry("700x500")

        self._build_ui()
        self._bind_shortcuts()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Text editor
        self.text = tk.Text(
            self,
            undo=True,
            wrap="word",
            font=("Consolas", 12),
            selectbackground="violet",
            selectforeground="black",
            insertbackground="white",
            bd=0,
            highlightthickness=0
        )
        self.text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.text.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_frame = ttk.Frame(self)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.columnconfigure(1, weight=1)

        # Sinistra (cursor)
        self.status_left = ttk.Label(self.status_frame, text="Riga 1, Col 0")
        self.status_left.grid(row=0, column=0, sticky="w", padx=5)

        # Destra (stats)
        self.status_right = ttk.Label(self.status_frame, text="0 parole, 0 caratteri")
        self.status_right.grid(row=0, column=1, sticky="e", padx=5)

        # Eventi per aggiornare la status bar
        self.text.bind("<KeyRelease>", self._update_status)
        self.text.bind("<ButtonRelease>", self._update_status)

        # Create menu:
        my_menu = tk.Menu(self)

        # -------------------
        # FILE
        # -------------------
        file_menu = tk.Menu(my_menu, tearoff=0)

        file_menu.add_command(label="Nuovo", command=self._new_file)
        file_menu.add_command(label="Apri", command=self._open_file)
        file_menu.add_command(label="Salva", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.destroy)

        my_menu.add_cascade(label="File", menu=file_menu)

        # -------------------
        # EDIT
        # -------------------
        edit_menu = tk.Menu(my_menu, tearoff=0)

        edit_menu.add_command(label="Undo", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Copia", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Incolla", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Taglia", command=lambda: self.text.event_generate("<<Cut>>"))

        my_menu.add_cascade(label="Modifica", menu=edit_menu)

        # -------------------
        # VIEW
        # -------------------
        view_menu = tk.Menu(my_menu, tearoff=0)

        view_menu.add_command(label="Toggle Dark Mode", command=self._toggle_theme)

        my_menu.add_cascade(label="Vista", menu=view_menu)

        # -------------------
        # HELP
        # -------------------
        help_menu = tk.Menu(my_menu, tearoff=0)

        help_menu.add_command(label="Info", command=self._show_about)

        my_menu.add_cascade(label="Aiuto", menu=help_menu)

        # -------------------
        # ATTIVA MENU
        # -------------------
        self.config(menu=my_menu)
    def _bind_shortcuts(self):
        self.bind("<Control-s>", self._save_file)
        self.bind("<Control-o>", self._open_file)

    def _update_status(self, event=None):
        cursor = self.text.index(tk.INSERT)
        row, col = cursor.split(".")

        # aggiorna posizione
        self.status_left.config(text=f"Riga {row}, Col {col}")

        # contenuto
        content = self.text.get("1.0", tk.END)

        chars = len(content) - 1  # togli newline finale
        words = len(content.split())

        self.status_right.config(text=f"{words} parole, {chars} caratteri")

    def _save_file(self, event=None):
        content = self.text.get("1.0", tk.END)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            with open(file_path, "w") as f:
                f.write(content)

            print("Salvato:", file_path)

    def _open_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            with open(file_path, "r") as f:
                content = f.read()

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)

            print("Aperto:", file_path)


if __name__ == "__main__":
    app = EditorWindow()
    app.mainloop()
