import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


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

def encrypt(data, psw):
    salt = os.urandom(16)
    key = derive_key(psw, salt)
    f = Fernet(key)
    if isinstance(data, str):
        data = data.encode("utf-8")

    token = f.encrypt(data)
    return salt + token

def decrypt(data, psw):
    salt, token = data[:16], data[16:]
    key = derive_key(psw, salt)
    f = Fernet(key)
    return(f.decrypt(token))


if __name__ == "__main__":
    print("hello world")
