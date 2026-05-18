import json
import logging
from pathlib import Path
from typing import Any
from platformdirs import user_config_dir, user_data_dir


# ── Costanti ──────────────────────────────────────────────────────────────────


APP_NAME    = "CipherDiary"
APP_AUTHOR  = "cipher-diary"
CONFIG_FILE = "config.json"
VERSION     = "1.0"

CONFIG_DIR      = Path(user_config_dir(APP_NAME, APP_AUTHOR))
DATA_DIR        = Path(user_data_dir(APP_NAME, APP_AUTHOR))
DEFAULT_DB_PATH = DATA_DIR / "diario.db.enc"
DEFAULT_AUTO_SAVE_PATH = DATA_DIR / "autosave.enc"

# ── Default ───────────────────────────────────────────────────────────────────

DEFAULT_CONFIG: dict[str, Any] = {
    "version": VERSION,
    "diary": {
        "autosave_path" : str(DEFAULT_DB_PATH),
        "db_path": str(DEFAULT_DB_PATH),
        "name": "Il mio diario",
    },
    "security": {
        "lock_after_minutes": 5,
        "clear_clipboard_on_lock": True,
    },
    "ui": {
        "theme": "light",
        "font_family": "Segoe UI",
        "font_size": 13,
        "window_width": 900,
        "window_height": 620,
    },
}

log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────

class Config:


    def __init__(self, data: dict[str, Any], path: Path):
        def print_file_content(path: str | Path) -> None:
            p = Path(path)

            if not p.exists():
                print("File non trovato:", p)
                return

            try:
                content = p.read_text(encoding="utf-8")
                print(content)
            except Exception as e:
                print("Errore lettura file:", e)

        print_file_content(CONFIG_DIR)
        self._data = data
        self._path = path


    @classmethod
    def load(cls, config_path: Path | None = None) -> "Config":
        path = config_path or (CONFIG_DIR / CONFIG_FILE)


        if not path.exists():
            cfg = cls(_deep_copy(DEFAULT_CONFIG), path)
            cfg._ensure_dirs()
            cfg.save()
            return cfg

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            data = _merge(DEFAULT_CONFIG, raw)
            cfg = cls(data, path)
            if data != raw:
                cfg.save()
            return cfg

        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Config corrotto (%s), uso il default", exc)
            cfg = cls(_deep_copy(DEFAULT_CONFIG), path)
            cfg._ensure_dirs()
            cfg.save()
            return cfg

    # ── Lettura / scrittura ───────────────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        return _get_nested(self._data, key, default)

    def set(self, key: str, value: Any) -> None:
        _set_nested(self._data, key, value)

    def save(self) -> None:
        self._ensure_dirs()
        try:
            self._path.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            raise
    # ── Shortcuts ─────────────────────────────────────────────────────────────

    @property
    def db_path(self) -> Path:
        return Path(self.get("diary.db_path"))
    @property
    def autosave_path(self) -> Path:
        return Path(self.get("diary.autosave_path"))


    def diary_path(self, path: "Path | str") -> None:
        base_path = Path(path)

        db_path = base_path.with_suffix(".diario.db.enc")
        autosave_path = base_path.with_suffix(".autosave.enc")

        self.set("diary.db_path", str(db_path))
        self.set("diary.autosave_path", str(autosave_path))

    @property
    def lock_after_minutes(self) -> int:
        return int(self.get("security.lock_after_minutes", 5))

    @property
    def theme(self) -> str:
        return self.get("ui.theme", "dark")

    @property
    def font_size(self) -> int:
        return int(self.get("ui.font_size", 13))

    @property
    def window_size(self) -> tuple[int, int]:
        return (int(self.get("ui.window_width", 900)),
                int(self.get("ui.window_height", 620)))

    @window_size.setter
    def window_size(self, size: tuple[int, int]) -> None:
        self.set("ui.window_width",  size[0])
        self.set("ui.window_height", size[1])

    '''
        def _ensure_dirs(self) -> None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            DATA_DIR.mkdir(parents=True, exist_ok=True)
    '''
    def _ensure_dirs(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_nested(d: dict, key: str, default: Any = None) -> Any:
    cur = d
    for k in key.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

def _set_nested(d: dict, key: str, value: Any) -> None:
    keys = key.split(".")
    cur  = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value

def _deep_copy(d: Any) -> Any:
    return json.loads(json.dumps(d))

def _merge(default: dict, override: dict) -> dict:
    result = _deep_copy(default)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _merge(result[k], v)
        else:
            result[k] = v
    return result

# ── Istanza globale ───────────────────────────────────────────────────────────

cfg: "Config | None" = None

def init_config(config_path: "Path | None" = None) -> Config:
    global cfg
    cfg = Config.load(config_path)
    return cfg