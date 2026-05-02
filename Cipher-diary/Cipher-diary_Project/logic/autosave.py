# autosave.py
from pathlib import Path
from core.crypto import encrypt, decrypt

AUTOSAVE_PATH = Path(".autosave.enc")
AUTOSAVE_INTERVAL_MS = 30_000  # 30 secondi


def save(content: str, password: str) -> None:
    AUTOSAVE_PATH.write_bytes(encrypt(content.encode(), password))


def load(password: str) -> str | None:
    if not AUTOSAVE_PATH.exists():
        return None
    try:
        return decrypt(AUTOSAVE_PATH.read_bytes(), password).decode()
    except Exception:
        return None


def delete() -> None:
    AUTOSAVE_PATH.unlink(missing_ok=True)


def exists() -> bool:
    return AUTOSAVE_PATH.exists()