# controller.py
from pathlib import Path
from data.db import Database
from core.config import cfg

def salva_pagina(
        filename: str,
        password: str,
        meta: dict,
        db_path: Path = cfg.diary_path
) -> None:

    pagina = {**meta, "filename": filename}

    with Database(password=password, db_path=db_path) as db:
        db.insert_pagina(pagina)