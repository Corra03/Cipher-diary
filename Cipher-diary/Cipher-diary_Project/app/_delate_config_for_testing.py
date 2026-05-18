
from pathlib import Path

BASE_DIR = Path(r"C:\Users\asus\AppData\Local\cipher-diary\CipherDiary")

files_to_delete = [
    BASE_DIR / "config.json",
    BASE_DIR / "diario.db.enc"
]

for file_path in files_to_delete:
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"Eliminato: {file_path}")
        except Exception as e:
            print(f"Errore eliminando {file_path}: {e}")
    else:
        print(f"Non trovato: {file_path}")