# db.py
import sqlite3
import tempfile
import os
from pathlib import Path
from core.crypto import encrypt, decrypt

DEFAULT_DB_ENC_PATH = Path("diario.db.enc")


class Database:
    def __init__(self, password: str, db_path: Path = DEFAULT_DB_ENC_PATH):
        self.password = password
        self.db_path = db_path
        self._tmp_fd, tmp_name = tempfile.mkstemp(suffix=".db")
        os.close(self._tmp_fd)
        self._tmp_path = Path(tmp_name)
        self._load()
        self.conn = sqlite3.connect(self._tmp_path)
        self._init_schema()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _load(self):
        if self.db_path.exists():
            data = self.db_path.read_bytes()
            try:
                self._tmp_path.write_bytes(decrypt(data, self.password))
            except Exception as e:
                self._tmp_path.unlink(missing_ok=True)
                raise ValueError("Password errata o database corrotto.") from e

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS pagine (
                filename    TEXT PRIMARY KEY,
                data        TEXT,
                ora_inizio  TEXT,
                ora_fine    TEXT,
                titolo      TEXT,
                mood        TEXT,
                parole      INTEGER,
                caratteri   INTEGER
            );

            CREATE TABLE IF NOT EXISTS tag (
                filename    TEXT NOT NULL REFERENCES pagine(filename) ON DELETE CASCADE,
                tag         TEXT NOT NULL,
                PRIMARY KEY (filename, tag)
            );
        """)
        self.conn.commit()

    def insert_pagina(self, meta: dict):
        tags = meta.pop("tag", [])

        self.conn.execute("""
            INSERT OR REPLACE INTO pagine
                (filename, data, ora_inizio, ora_fine, titolo, mood, parole, caratteri)
            VALUES
                (:filename, :data, :ora_inizio, :ora_fine, :titolo, :mood, :parole, :caratteri)
        """, meta)

        self.conn.execute("DELETE FROM tag WHERE filename = ?", (meta["filename"],))
        self.conn.executemany(
            "INSERT INTO tag (filename, tag) VALUES (?, ?)",
            [(meta["filename"], t.strip()) for t in tags if t.strip()]
        )

        self.conn.commit()

    def cerca_per_tag(self, tag: str) -> list:
        return self.conn.execute("""
            SELECT p.*
            FROM pagine p
            JOIN tag t ON t.filename = p.filename
            WHERE lower(t.tag) = lower(?)
        """, (tag.strip(),)).fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        try:
            data = self._tmp_path.read_bytes()
            self.db_path.write_bytes(encrypt(data, self.password))
        finally:
            self._tmp_path.unlink(missing_ok=True)