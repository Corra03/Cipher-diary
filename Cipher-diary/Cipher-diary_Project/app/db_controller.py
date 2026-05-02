# controller.py
from pathlib import Path
from data.db import Database, DEFAULT_DB_ENC_PATH


def salva_pagina(
        filename: str,
        password: str,
        meta: dict,
        db_path: Path = DEFAULT_DB_ENC_PATH,
) -> None:

    pagina = {**meta, "filename": filename}

    with Database(password=password, db_path=db_path) as db:
        db.insert_pagina(pagina)