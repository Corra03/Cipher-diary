import base64
import os
import sqlite3
import sys
import tempfile
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#PATH GLOBALE:

path = r"C:\Users\asus\Desktop\programma\Python_2.0\Progettti\Diario_cifrato\Cipher-diary\Cipher-diary_Project\diario.db.enc"




def derive_key(psw, salt):
    psw = psw.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(psw))
    return key


def decrypt_file(data, psw):
    salt, token = data[:16], data[16:]
    key = derive_key(psw, salt)
    f = Fernet(key)
    return f.decrypt(token)


def print_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    for (table,) in tables:
        print(f"\n=== TABLE: {table} ===")
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        for row in rows:
            print(row)

    conn.close()


if __name__ == "__main__":
    print("Path del file cifrato SQLite: ", end="", flush=True)
    path = sys.stdin.readline().strip().strip('"')
    path = path
    print("Password: ", end="", flush=True)
    password = sys.stdin.readline().strip()

    with open(path, "rb") as f:
        encrypted_data = f.read()

    decrypted_db = decrypt_file(encrypted_data, password)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        tmp.write(decrypted_db)
        tmp_path = tmp.name

    try:
        print_sqlite(tmp_path)
    finally:
        os.remove(tmp_path)