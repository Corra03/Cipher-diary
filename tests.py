import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

psw = input("Insert password: ").encode()
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_200_000,
)
key = base64.urlsafe_b64encode(kdf.derive(psw))
f = Fernet(key)
token = f.encrypt(b"Secret message!")
with open("data.bin", "wb") as file:
    file.write(salt + token)
    print(token)

with open("data.bin", "rb") as file:
    data = file.read()
    salt, token = data[:16], data[16:]
    print(f.decrypt(token))
