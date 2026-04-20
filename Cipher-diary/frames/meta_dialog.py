import tkinter as tk
from tkinter import ttk
from datetime import datetime

TAGS_PREDEFINITI = (
    "università", "lavoro", "stress", "amore", "soldi",
    "studio", "futuro", "riflessioni", "dubbi",
    "presente", "passato", "traumi", "famiglia",
    "amicizia", "salute", "viaggi", "creatività", "obiettivi"
)

class MetaDialog(tk.Toplevel):
    def __init__(self, parent, on_confirm, ora_inizio: str, parole: int, caratteri: int):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.ora_inizio = ora_inizio
        self.mood_var = tk.IntVar(value=0)
        self.parole = parole
        self.caratteri = caratteri
        self.title("Prima di salvare...")
        self.geometry("350x550")
        self.resizable(False, False)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        self._build_titolo(container, row=0)
        self._build_info_automatiche(container, row=3)
        self._build_mood(container, row=7)
        self._build_tags(container, row=9)
        self._build_confirm_btn(container, row=15)

    def _build_titolo(self, parent, row):
        ttk.Label(parent, text="Titolo (opzionale)").grid(
            row=row, column=0, sticky="w", pady=(0, 2))
        self.entry_titolo = ttk.Entry(parent)
        self.entry_titolo.grid(row=row+1, column=0, sticky="ew", pady=(0, 15))

    def _build_info_automatiche(self, parent, row):
        ora_fine = datetime.now().strftime("%H:%M")
        data_oggi = datetime.now().strftime("%Y-%m-%d")

        info_frame = ttk.Frame(parent)
        info_frame.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        info_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(info_frame, text="Data").grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, text="Inizio").grid(row=0, column=1, sticky="w")
        ttk.Label(info_frame, text="Fine").grid(row=0, column=2, sticky="w")

        ttk.Label(info_frame, text=data_oggi, foreground="gray").grid(row=1, column=0, sticky="w")
        ttk.Label(info_frame, text=self.ora_inizio, foreground="gray").grid(row=1, column=1, sticky="w")
        ttk.Label(info_frame, text=ora_fine, foreground="gray").grid(row=1, column=2, sticky="w")

        ttk.Label(info_frame, text="Parole").grid(row=2, column=0, sticky="w")
        ttk.Label(info_frame, text="Caratteri").grid(row=2, column=1, sticky="w")

        ttk.Label(info_frame, text=self.parole, foreground="gray").grid(row=3, column=0, sticky="w")
        ttk.Label(info_frame, text=self.caratteri, foreground="gray").grid(row=3, column=1, sticky="w")

        self._data = data_oggi
        self._ora_fine = ora_fine

    def _build_mood(self, parent, row):
        ttk.Label(parent, text="Come stai?").grid(
            row=row, column=0, sticky="w", pady=(0, 5))

        mood_frame = ttk.Frame(parent)
        mood_frame.grid(row=row+1, column=0, sticky="ew", pady=(0, 15))

        MOODS = ["😞", "😕", "😐", "🙂", "😄"]

        for i, emoji in enumerate(MOODS):
            ttk.Radiobutton(
                mood_frame,
                text=emoji,
                variable=self.mood_var,
                value=i + 1,
            ).grid(row=0, column=i, padx=5)

    def _build_tags(self, parent, row):
        ttk.Label(parent, text="Tag").grid(row=row, column=0, sticky="w", pady=(0, 5))

        # frame scrollabile per le checkbox
        tags_frame = ttk.Frame(parent)
        tags_frame.grid(row=row + 1, column=0, sticky="ew", pady=(0, 10))

        self.tag_vars = {}
        for i, tag in enumerate(TAGS_PREDEFINITI):
            var = tk.BooleanVar()
            self.tag_vars[tag] = var
            ttk.Checkbutton(tags_frame, text=tag, variable=var).grid(
                row=i // 3, column=i % 3, sticky="w", padx=5
            )

        # campo libero
        ttk.Label(parent, text="Altri tag (separati da virgola)").grid(
            row=row + 2, column=0, sticky="w", pady=(5, 2))
        self.entry_tags_custom = ttk.Entry(parent)
        self.entry_tags_custom.grid(row=row + 3, column=0, sticky="ew")

    def _build_confirm_btn(self, parent, row):
        ttk.Button(parent, text="Salva", command=self._confirm).grid(
            row=row, column=0, sticky="ew", pady=(10, 0))

    def _confirm(self):
        tags_selezionati = [tag for tag, var in self.tag_vars.items() if var.get()]
        tags_custom = [t.strip() for t in self.entry_tags_custom.get().split(",") if t.strip()]
        tutti_i_tag = tags_selezionati + tags_custom
        meta = {
            "titolo": self.entry_titolo.get().strip() or None,
            "data": self._data,
            "ora_inizio": self.ora_inizio,
            "ora_fine": self._ora_fine,
            "mood": self.mood_var.get() or None,  # None se non selezionato
            "tag": tutti_i_tag
        }
        self.on_confirm(meta)
        self.destroy()
