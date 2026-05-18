from core.crypto import encrypt, decrypt
from core.config import cfg, init_config

AUTOSAVE_INTERVAL_MS = 30_000

def _path():
    c = cfg
    return c.autosave_path

def save(content: str, password: str) -> None:
    _path().write_bytes(encrypt(content.encode(), password))

def load(password: str) -> str | None:
    if not _path().exists():
        return None
    try:
        return decrypt(_path().read_bytes(), password).decode()
    except Exception:
        return None

def delete() -> None:
    _path().unlink(missing_ok=True)

def exists() -> bool:
    return _path().exists()