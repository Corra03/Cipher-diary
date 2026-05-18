import tkinter as tk
from tkinter import ttk
from . import utils as ut
from tkinter import filedialog
from core.config import init_config
from .theme import BG, SURFACE, ACCENT, FG, FG_MUTED

# ── Helpers ───────────────────────────────────────────────────────────────────

def _section(parent, title: str, row: int) -> ttk.Frame:
    outer = tk.Frame(parent, bg=BG)
    outer.grid(row=row, column=0, columnspan=3,
               sticky="ew", padx=30, pady=(18, 4))
    outer.columnconfigure(1, weight=1)

    tk.Label(outer, text=title.upper(), bg=BG,
             fg=FG_MUTED, font=("Courier New", 8, "bold"),
             anchor="w").grid(row=0, column=0, sticky="w")

    sep = tk.Frame(outer, bg=FG_MUTED, height=1)
    sep.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=6)

    inner = tk.Frame(outer, bg=SURFACE,
                     highlightbackground=ACCENT,
                     highlightthickness=0)
    inner.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
    inner.columnconfigure(1, weight=1)
    return inner


class Options(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        cfg = init_config()
        self._pending_theme  = cfg.theme
        self._pending_width  = cfg.window_size[0]
        self._pending_height = cfg.window_size[1]
        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure(".", background=BG, foreground=FG, font=("Courier New", 11))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG)

        s.configure("Options.TButton",
                    background=SURFACE, foreground=FG,
                    relief="flat", borderwidth=0, padding=(14, 8))
        s.map("Options.TButton",
              background=[("active", "#1f2d4a")],
              foreground=[("active", ACCENT)])

        s.configure("Primary.TButton",
                    background=ACCENT, foreground="#ffffff",
                    relief="flat", borderwidth=0, padding=(14, 10),
                    font=("Courier New", 11, "bold"))
        s.map("Primary.TButton",
              background=[("active", "#c73652")])

        s.configure("TEntry",
                    fieldbackground=SURFACE, foreground=FG,
                    insertcolor=ACCENT, borderwidth=0,
                    relief="flat", padding=6)

    def _start_resize(self):
        self._resize_win = tk.Toplevel(self.winfo_toplevel(), bg=BG)
        self._resize_win.title("Cipher-diary — anteprima dimensioni")
        self._resize_win.geometry(f"{self._pending_width}x{self._pending_height}")
        self._resize_win.resizable(True, True)
        self._resize_win.protocol("WM_DELETE_WINDOW", self._stop_resize)

        # bottone ancorato in basso, tutto il resto è spazio libero
        frame_bottom = tk.Frame(self._resize_win, bg=BG)
        frame_bottom.pack(side="bottom", fill="x", padx=30, pady=16)

        tk.Label(frame_bottom,
                 text="Trascina i bordi, poi premi Done",
                 bg=BG, fg=FG_MUTED,
                 font=("Courier New", 9)).pack(side="left")

        ttk.Button(frame_bottom, text="✔  Done",
                   style="Primary.TButton",
                   command=self._stop_resize).pack(side="right")

    def _stop_resize(self):
        self._pending_width = self._resize_win.winfo_width()
        self._pending_height = self._resize_win.winfo_height()
        if self._resize_win.winfo_exists():
            self._resize_win.destroy()

    def save(self):
        from core.config import cfg
        cfg.set("diary.name",                       self.entry_name.get())
        cfg.set("security.lock_after_minutes",      int(self.close_time.get()))
        cfg.set("security.clear_clipboard_on_lock", self.clear_clipboard.get())
        cfg.set("ui.theme",   "dark" if self.is_dark.get() else "light")
        cfg.window_size = (self._pending_width, self._pending_height)
        cfg.save()

    def _reset_to_default(self):
        from core.config import DEFAULT_CONFIG

        self._pending_width  = DEFAULT_CONFIG["ui"]["window_width"]
        self._pending_height = DEFAULT_CONFIG["ui"]["window_height"]

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, DEFAULT_CONFIG["diary"]["name"])

        self.close_time.delete(0, tk.END)
        self.close_time.insert(0, DEFAULT_CONFIG["security"]["lock_after_minutes"])

        default_clip = DEFAULT_CONFIG["security"]["clear_clipboard_on_lock"]
        self.clear_clipboard.set(default_clip)
        self.btn_clipboard.config(
            text="🔒  Clear clipboard on lock   ✓" if default_clip
                 else "🔓  Clear clipboard on lock"
        )

        default_dark = DEFAULT_CONFIG["ui"]["theme"] == "dark"
        self.is_dark.set(default_dark)
        self.btn_theme.config(
            text="🌙    Dark mode" if default_dark else "☀️ Light mode"
        )

    def _build_ui(self):
        # ── Container scrollabile ─────────────────────────────────────────────
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = tk.Frame(self, bg=BG)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0, bd=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))

        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(win_id, width=e.width)
        )

        # scroll con rotella del mouse
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # ── Titolo ────────────────────────────────────────────────────────────
        tk.Label(scrollable_frame, text="⚙  Settings", bg=BG, fg=FG,
                 font=("Courier New", 16, "bold"),
                 anchor="w").grid(row=0, column=1, columnspan=3,
                                  sticky="ew", padx=30, pady=(24, 0))
        ut.add_back_button(self)

        # ── Diary ─────────────────────────────────────────────────────────────
        sec_diary = _section(scrollable_frame, "Diary", row=1)

        tk.Label(sec_diary, text="Name", bg=SURFACE, fg=FG_MUTED,
                 font=("Courier New", 10)).grid(row=0, column=0,
                                                padx=(16, 8), pady=12, sticky="w")
        self.entry_name = ttk.Entry(sec_diary)
        self.entry_name.insert(0, "Il mio Diario")
        self.entry_name.grid(row=0, column=1, padx=(0, 16), pady=12, sticky="ew")

        # ── Security ──────────────────────────────────────────────────────────
        sec_sec = _section(scrollable_frame, "Security", row=2)
        sec_sec.columnconfigure(1, weight=1)

        tk.Label(sec_sec, text="Auto-lock (min)", bg=SURFACE, fg=FG_MUTED,
                 font=("Courier New", 10)).grid(row=0, column=0,
                                                padx=(16, 8), pady=12, sticky="w")
        self.close_time = tk.Spinbox(sec_sec, from_=1, to=100,
                                     bg=SURFACE, fg=FG,
                                     buttonbackground=SURFACE,
                                     relief="flat", bd=0, width=5,
                                     font=("Courier New", 11),
                                     insertbackground=ACCENT)
        self.close_time.grid(row=0, column=1, padx=(0, 16), pady=12, sticky="w")

        self.clear_clipboard = tk.BooleanVar(value=False)

        def toggle_clip():
            self.clear_clipboard.set(not self.clear_clipboard.get())
            self.btn_clipboard.config(
                text="🔒  Clear clipboard on lock   ✓" if self.clear_clipboard.get()
                     else "🔓  Clear clipboard on lock")

        self.btn_clipboard = ttk.Button(sec_sec, text="🔓  Clear clipboard on lock",
                                        style="Options.TButton", command=toggle_clip)
        self.btn_clipboard.grid(row=1, column=0, columnspan=2,
                                padx=12, pady=(0, 12), sticky="ew")

        # ── Interface ─────────────────────────────────────────────────────────
        sec_ui = _section(scrollable_frame, "Interface", row=3)
        sec_ui.columnconfigure(0, weight=1)
        sec_ui.columnconfigure(1, weight=1)

        self.is_dark = tk.BooleanVar(value=False)

        def toggle_theme():
            self.is_dark.set(not self.is_dark.get())
            self.btn_theme.config(
                text="🌙    Dark mode" if self.is_dark.get() else "☀️ Light mode")

        self.btn_theme = ttk.Button(sec_ui, text="☀️ Light mode",
                                    style="Options.TButton", command=toggle_theme)
        self.btn_theme.grid(row=0, column=0, padx=(12, 4), pady=12, sticky="ew")

        self.btn_set_size = ttk.Button(sec_ui, text="⤢  Resize window",
                                       style="Options.TButton",
                                       command=self._start_resize)
        self.btn_set_size.grid(row=0, column=1, padx=(4, 12), pady=12, sticky="ew")

        # ── Azioni ────────────────────────────────────────────────────────────
        btn_reset = ttk.Button(scrollable_frame, text="↺  Ripristina default",
                               style="Options.TButton",
                               command=self._reset_to_default)
        btn_reset.grid(row=10, column=0, columnspan=3,
                       padx=30, pady=(0, 8), sticky="ew")

        btn_save = ttk.Button(scrollable_frame, text="💾  Save settings",
                              style="Primary.TButton", command=self.save)
        btn_save.grid(row=12, column=0, columnspan=3,
                      padx=30, pady=24, sticky="ew")





'''
#COLORLESS
import tkinter as tk
from tkinter import ttk
from . import utils as ut
from tkinter import filedialog
from core.config import init_config

class Options(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        cfg = init_config()
        self._pending_theme  = cfg.theme                  # "light" / "dark"
        self._pending_width  = cfg.window_size[0]
        self._pending_height = cfg.window_size[1]
        self._build_ui()

    def _start_resize(self):
        self.master.resizable(True, True)

        self._resize_win = tk.Toplevel(self.master)
        self._resize_win.title("Resize")
        self._resize_win.attributes("-topmost", True)
        self._resize_win.protocol("WM_DELETE_WINDOW", self._stop_resize)
        ttk.Label(
            self._resize_win,
            text="Resize the main window to the desired size,\nthen press Done."
        ).pack(padx=20, pady=10)
        ttk.Button(self._resize_win, text="✔ Done", command=self._stop_resize).pack(padx=20, pady=20)

        self._resize_win.grab_set()
        self.master.wait_window(self._resize_win)

    def _stop_resize(self):
        self._pending_width  = self.master.winfo_width()
        self._pending_height = self.master.winfo_height()
        self.master.resizable(False, False)
        if hasattr(self, "_resize_win") and self._resize_win.winfo_exists():
            self._resize_win.destroy()

    def save(self):
        from core.config import cfg

        cfg.set("diary.name", self.entry_name.get())
        cfg.set("security.lock_after_minutes", int(self.close_time.get()))
        cfg.set("security.clear_clipboard_on_lock", self.clear_clipboard.get())
        cfg.set("ui.theme", "dark" if self.is_dark.get() else "light")
        cfg.set("ui.window_width", self._pending_width)
        cfg.set("ui.window_height", self._pending_height)
        cfg.save()

    def _build_ui(self):
        def insert_path():
            path = filedialog.askdirectory(
                title="Select destination folder"
            )

            print(path)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        ut.add_back_button(self)

        #--------------------------------------------------------------------------
        # NOME
        #--------------------------------------------------------------------------


        label = ttk.Label(self, text="Inserisci Il nome del diario")
        label.grid(row=1, column=0, pady=5)

        self.entry_name = ttk.Entry(self)
        self.entry_name.insert(0, "Il mio Diario")
        self.entry_name.grid(row=1, column=1, padx=40, pady=5)

        #--------------------------------------------------------------------------
        # chiusura dopo n min
        #--------------------------------------------------------------------------


        label = ttk.Label(self, text="Chiusura dopo Min: ")
        label.grid(row=2, column=0, pady=5)
        self.close_time = tk.Spinbox(
            self,
            from_=1,
            to=100
        )
        self.close_time.grid(row=2, column=1, pady=5)


        #--------------------------------------------------------------------------
        #pulizia clipboard
        #--------------------------------------------------------------------------

        self.clear_clipboard = tk.BooleanVar(value=False)

        def toggle():
            self.clear_clipboard.set(not self.clear_clipboard.get())
            btn_clipboard.config(text="do not clear_clipboard_on_lock" if self.clear_clipboard.get() else "clear_clipboard_on_lock")

        btn_clipboard = ttk.Button(self, text="clear_clipboard_on_lock", command=toggle)
        btn_clipboard.grid(row=3, column=0, columnspan=3, pady=5, padx=40, sticky="nsew")

        #--------------------------------------------------------------------------
        #tema
        #--------------------------------------------------------------------------

        self.is_dark = tk.BooleanVar(value=False)

        def toggle():
            self.is_dark.set(not self.is_dark.get())
            btn_theme.config(text="🌙  Dark mode" if self.is_dark.get() else "☀️ Light mode")

        btn_theme = ttk.Button(self, text="☀️ Light mode", command=toggle)
        btn_theme.grid(row=4, column=0, columnspan=3, pady=5, padx=40, sticky="nsew")

        #--------------------------------------------------------------------------
        #window width and high
        #--------------------------------------------------------------------------


        label_size = ttk.Label(self, text="Window size:")
        label_size.grid(row=5, column=0, pady=5, padx=10, sticky="e")

        self.btn_set_size = ttk.Button(
            self,
            text="Resize window",
            command=self._start_resize
        )
        self.btn_set_size.grid(row=5, column=1, columnspan=2, pady=5, padx=10, sticky="ew")

        #--------------------------------------------------------------------------
        #save
        #--------------------------------------------------------------------------

        btn_save = ttk.Button(self, text="💾 Salva", command=self.save)
        btn_save.grid(row=9, column=0, columnspan=3, pady=20, padx=40, sticky="nsew")

'''