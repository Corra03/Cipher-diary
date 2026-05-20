def _ask_diary_folder(cfg):
    import tkinter as tk
    from tkinter import ttk, filedialog

    root = tk.Tk()
    root.title("Benvenuto in Cipher-diary")
    root.resizable(False, False)
    root.geometry("420x260")
    root.columnconfigure(0, weight=1)

    tk.Label(root, text="Benvenuto in Cipher-diary",
             font=("Segoe UI", 13, "bold")).grid(
             row=0, column=0, pady=(30, 6), padx=40)

    tk.Label(root,
             text="Scegli la cartella dove verrà salvato\nil tuo diario cifrato.",
             font=("Segoe UI", 10), justify="center", fg="#555").grid(
             row=1, column=0, pady=(0, 20), padx=40)

    path_var = tk.StringVar(value=str(cfg.db_path.parent))

    frame_path = tk.Frame(root)
    frame_path.grid(row=2, column=0, padx=40, sticky="ew")
    frame_path.columnconfigure(0, weight=1)

    entry = ttk.Entry(frame_path, textvariable=path_var, state="readonly")
    entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    def browse():
        folder = filedialog.askdirectory(title="Scegli cartella diario")
        if folder:
            path_var.set(folder)

    ttk.Button(frame_path, text="Sfoglia", command=browse).grid(row=0, column=1)

    def confirm():
        chosen = path_var.get()
        if chosen:
            cfg.diary_path(chosen + "/diario")
            cfg.save()
        root.destroy()

    ttk.Button(root, text="Inizia →", command=confirm).grid(
               row=3, column=0, pady=24, ipadx=10)

    root.mainloop()