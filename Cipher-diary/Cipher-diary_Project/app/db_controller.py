from data import db as Database
from pathlib import Path

DB_PATH = Path("diario.db.enc")

class DiarioService:
    def __init__(self, get_password_fn):
        self._get_password = get_password_fn
        self._db: Database | None = None


    def build_db(self, psw, meta):
        try:
            Database._load()
