# db.py
import sqlite3
import tempfile
import os
from pathlib import Path
from core.cyber import encrypt, decrypt

DB_ENC_PATH = Path("diario.db.enc")

class Database:
    def __init__(self, password: str):
        self.password = password
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp_path = Path(self._tmp.name)
        self._tmp.close()
        self._load()
        self.conn = sqlite3.connect(self._tmp_path)
        self._init_schema()

    def _load(self):
        # se esiste già un db cifrato lo decifra nel tmp
        if DB_ENC_PATH.exists():
            data = DB_ENC_PATH.read_bytes()
            self._tmp_path.write_bytes(decrypt(data, self.password))

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pagine (
                filename TEXT PRIMARY KEY,
                data TEXT,
                ora TEXT,
                titolo TEXT,
                mood TEXT,
                luogo TEXT,
                tag TEXT,
                parole INTEGER,
                caratteri INTEGER
            )
        """)
        self.conn.commit()

    def insert_pagina(self, meta: dict):
        self.conn.execute("""
            INSERT OR REPLACE INTO pagine
            VALUES (:filename, :data, :ora, :titolo, :mood, :luogo, :tag, :parole, :caratteri)
        """, meta)
        self.conn.commit()

    def cerca_per_tag(self, tag: str):
        return self.conn.execute(
            "SELECT * FROM pagine WHERE tag LIKE ?", (f"%{tag}%",)
        ).fetchall()

    def close(self):
        self.conn.close()
        # cifra e salva
        data = self._tmp_path.read_bytes()
        DB_ENC_PATH.write_bytes(encrypt(data, self.password))
        # cancella il temporaneo
        os.unlink(self._tmp_path)