import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataclasses import dataclass, field
from datetime import datetime

# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Theme:
    name: str
    bg: str
    fg: str
    insert_bg: str
    select_bg: str
    select_fg: str
    status_bg: str
    status_fg: str
    font_family: str = "Consolas"
    font_size: int = 12


DARK_THEME = Theme(
    name="dark",
    bg="#1e1e2e",
    fg="#cdd6f4",
    insert_bg="#f5c2e7",
    select_bg="#585b70",
    select_fg="#cdd6f4",
    status_bg="#181825",
    status_fg="#a6adc8",
)

LIGHT_THEME = Theme(
    name="light",
    bg="#ffffff",
    fg="#1e1e2e",
    insert_bg="#1e1e2e",
    select_bg="violet",
    select_fg="black",
    status_bg="#e8eaf0",
    status_fg="#555770",
)


# ---------------------------------------------------------------------------
# Editor logic (pure state, no Tkinter dependency)
# ---------------------------------------------------------------------------

class EditorState:
    def __init__(self):
        self.current_file: str | None = None
        self.is_modified: bool = False
        self.theme: Theme = LIGHT_THEME

    def toggle_theme(self) -> Theme:
        self.theme = LIGHT_THEME if self.theme.name == "dark" else DARK_THEME
        return self.theme

    @staticmethod
    def count_stats(text: str) -> tuple[int, int]:
        lines = text.splitlines()

        filtered_lines = [
            line for line in lines
            if not set(line.strip()) <= {"_", "=", "-", " "}
        ]

        filtered_text = "\n".join(filtered_lines)

        chars = len(filtered_text)
        words = len(filtered_text.split()) if filtered_text.strip() else 0

        return words, chars


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class EditorApp(tk.Tk):
    """
    Root window. Owns the state and wires together UI and logic.
    Delegates UI construction to _build_ui() and event handling to _bind_events().
    """

    APP_TITLE = "Editor"
    MIN_WIDTH, MIN_HEIGHT = 500, 350

    def __init__(self):
        super().__init__()
        self.state = EditorState()

        self._configure_window()
        self._configure_style()
        self._build_ui()
        self._bind_events()
        self._apply_theme(self.state.theme)
        self._new_file()

    # ------------------------------------------------------------------
    # Window / style setup
    # ------------------------------------------------------------------

    def _configure_window(self):
        self.title(self.APP_TITLE)
        self.geometry("760x520")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _configure_style(self):
        self._style = ttk.Style(self)
        self._style.theme_use("clam")
        self._style.configure("Status.TFrame", relief="flat")
        self._style.configure("Status.TLabel", padding=(6, 3))

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        self._build_editor()
        self._build_status_bar()
        self._build_menu()

    def _build_editor(self):
        """Text widget + scrollbar in a sub-frame for clean layout."""
        editor_frame = tk.Frame(self, bd=0, highlightthickness=0)
        editor_frame.grid(row=0, column=0, sticky="nsew")
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)

        self.text = tk.Text(
            editor_frame,
            undo=True,
            wrap="word",
            font=(EditorState().theme.font_family, EditorState().theme.font_size),
            bd=0,
            highlightthickness=0,
            selectbackground="violet",
            selectforeground="black",
            relief="flat",
            padx=12,
            pady=10,
        )
        self.text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=scrollbar.set)

    def _build_status_bar(self):
        """Two-column status bar: cursor position (left), stats (right)."""
        self._status_frame = ttk.Frame(self, style="Status.TFrame")
        self._status_frame.grid(row=1, column=0, sticky="ew")
        self._status_frame.columnconfigure(1, weight=1)

        self._lbl_cursor = ttk.Label(
            self._status_frame, text="Riga 1, Col 0", style="Status.TLabel"
        )
        self._lbl_cursor.grid(row=0, column=0, sticky="w")

        self._lbl_stats = ttk.Label(
            self._status_frame, text="0 parole · 0 caratteri", style="Status.TLabel"
        )
        self._lbl_stats.grid(row=0, column=1, sticky="e")

    def _build_menu(self):
        """Build the menu bar using a helper to reduce boilerplate."""
        menubar = tk.Menu(self, tearoff=0)

        file_items = [
            ("Nuovo",       "Ctrl+N", self._new_file),
            ("Apri…",       "Ctrl+O", self._open_file),
            ("Salva",       "Ctrl+S", self._save_file),
            ("Salva con nome…", None, self._save_file_as),
            None,  # separator
            ("Esci",        "Alt+F4", self.destroy),
        ]
        edit_items = [
            ("Annulla",  "Ctrl+Z", lambda: self.text.event_generate("<<Undo>>")),
            ("Ripristina","Ctrl+Y", lambda: self.text.event_generate("<<Redo>>")),
            None,
            ("Copia",    "Ctrl+C", lambda: self.text.event_generate("<<Copy>>")),
            ("Incolla",  "Ctrl+V", lambda: self.text.event_generate("<<Paste>>")),
            ("Taglia",   "Ctrl+X", lambda: self.text.event_generate("<<Cut>>")),
            None,
            ("Seleziona tutto", "Ctrl+A", self._select_all),
        ]
        view_items = [
            ("Attiva/Disattiva tema scuro", None, self._toggle_theme),
        ]
        help_items = [
            ("Informazioni…", None, self._show_about),
        ]
        inserisci_item = [
            ("Inserisci separatore", "Ctrl+K", self._insert_separator),
            ("Inserisci doppio separatore", "Ctrl+J", self._insert_doble_separator),
            ("Inserisci Data", "Ctrl+L", self._insert_date)
        ]

        for label, items in [
            ("File",     file_items),
            ("Modifica", edit_items),
            ("Vista",    view_items),
            ("Aiuto",    help_items),
            ("Inserisci", inserisci_item)
        ]:
            menubar.add_cascade(label=label, menu=self._make_menu(menubar, items))

        self.config(menu=menubar)

    @staticmethod
    def _make_menu(parent: tk.Menu, items: list) -> tk.Menu:
        """Build a Menu from a list of (label, accel, command) tuples or None (separator)."""
        menu = tk.Menu(parent, tearoff=0)
        for item in items:
            if item is None:
                menu.add_separator()
            else:
                label, accel, cmd = item
                kw = {"label": label, "command": cmd}
                if accel:
                    kw["accelerator"] = accel
                menu.add_command(**kw)
        return menu

    # ------------------------------------------------------------------
    # Event binding
    # ------------------------------------------------------------------

    def _bind_events(self):
        self.bind("<Control-n>", lambda e: self._new_file())
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-s>", lambda e: self._save_file())
        self.bind("<Control-S>", lambda e: self._save_file_as())   # Ctrl+Shift+S
        self.bind("<Control-a>", lambda e: self._select_all())
        self.bind("<Control-k>", lambda e: self._insert_separator())
        self.bind("<Control-j>", lambda e: self._insert_doble_separator())
        self.bind("<Control-l>", lambda e: self._insert_date())
        self.text.bind("<KeyRelease>",    self._on_text_changed)
        self.text.bind("<ButtonRelease>", self._on_text_changed)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------

    def _apply_theme(self, theme: Theme):
        """Apply color scheme to the text widget and status bar."""
        self.configure(bg=theme.bg)
        self.text.configure(
            bg=theme.bg,
            fg=theme.fg,
            insertbackground=theme.insert_bg,
            selectbackground=theme.select_bg,
            selectforeground=theme.select_fg,
            font=(theme.font_family, theme.font_size),
        )
        self._style.configure(
            "Status.TFrame",
            background=theme.status_bg,
        )
        self._style.configure(
            "Status.TLabel",
            background=theme.status_bg,
            foreground=theme.status_fg,
        )
        # Force label refresh (ttk doesn't always repaint on style change)
        for lbl in (self._lbl_cursor, self._lbl_stats):
            lbl.configure(style="Status.TLabel")

    def _toggle_theme(self):
        new_theme = self.state.toggle_theme()
        self._apply_theme(new_theme)

    # ------------------------------------------------------------------
    # Status bar update
    # ------------------------------------------------------------------

    def _on_text_changed(self, _event=None):
        self._update_cursor()
        self._update_stats()
        self.state.is_modified = True

    def _update_cursor(self):
        row, col = self.text.index(tk.INSERT).split(".")
        self._lbl_cursor.config(text=f"Riga {row}, Col {col}")

    def _update_stats(self):
        content = self.text.get("1.0", tk.END)
        words, chars = self.state.count_stats(content)
        self._lbl_stats.config(text=f"{words} parole · {chars} caratteri")

    def _refresh_title(self):
        name = self.state.current_file or "Senza nome"
        modified_flag = " •" if self.state.is_modified else ""
        self.title(f"{self.APP_TITLE} — {name}{modified_flag}")

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def _new_file(self):
        if not self._confirm_discard():
            return

        self.text.delete("1.0", tk.END)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        header = f"{timestamp}\n\n"
        self.text.insert("1.0", header)
        self.state.current_file = None
        self.state.is_modified = False
        self._refresh_title()
        self._update_stats()
    def _open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except OSError as exc:
            messagebox.showerror("Errore", f"Impossibile aprire il file:\n{exc}")
            return
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)
        self.state.current_file = path
        self.state.is_modified = False
        self._refresh_title()
        self._update_stats()

    def _save_file(self):
        if self.state.current_file:
            self._write_file(self.state.current_file)
        else:
            self._save_file_as()

    def _save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")],
        )
        if path:
            self._write_file(path)

    def _write_file(self, path: str):
        content = self.text.get("1.0", tk.END)
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except OSError as exc:
            messagebox.showerror("Errore", f"Impossibile salvare il file:\n{exc}")
            return
        self.state.current_file = path
        self.state.is_modified = False
        self._refresh_title()

    # ------------------------------------------------------------------
    # Edit helpers
    # ------------------------------------------------------------------

    def _select_all(self):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, tk.END)

    # ------------------------------------------------------------------
    # Insert Elements
    # ------------------------------------------------------------------
    def _insert_separator_base(self, char="-", length=80):
        separator = "\n" + char * length + "\n\n"
        self.text.insert(tk.INSERT, separator)
        self.state.is_modified = True

    def _insert_separator(self):
        self._insert_separator_base("_")

    def _insert_doble_separator(self):
        self._insert_separator_base("=")
    def _insert_date(self):
        timestamp = datetime.now().strftime("\n%d/%m/%Y %H:%M:%S\n")
        self.text.insert(tk.INSERT, timestamp)
        self.state.is_modified = True



    # ------------------------------------------------------------------
    # Window / lifecycle
    # ------------------------------------------------------------------

    def _confirm_discard(self) -> bool:
        """Returns True if it's safe to discard the current document."""
        if not self.state.is_modified:
            return True
        answer = messagebox.askyesnocancel(
            "Modifiche non salvate",
            "Il documento ha modifiche non salvate.\nVuoi salvare prima di continuare?",
        )
        if answer is None:       # Cancel
            return False
        if answer:               # Yes → save, then proceed
            self._save_file()
        return True              # No → discard

    def _on_close(self):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        footer = f"\n\n{timestamp}\n"

        self.text.insert(tk.END, footer)
        self.state.is_modified = True
        if self._confirm_discard():
            self.destroy()

    def _show_about(self):
        messagebox.showinfo(
            "Informazioni",
            "Editor v2.0\n\nUn semplice editor di testo in Python + Tkinter.\n\n"
            "Funzionalità:\n"
            "  • Tema chiaro / scuro\n"
            "  • Contatore parole e caratteri\n"
            "  • Rilevamento modifiche non salvate\n"
            "  • Codifica UTF-8",
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = EditorApp()
    app.mainloop()