import pytest
from crypto import encrypt, decrypt
from cryptography.fernet import InvalidToken

def test_encrypt_decrypt():
    testo = "ciao mondo"
    encrypted = encrypt(testo, "miapassword")
    decripted_text =(decrypt(encrypted, "miapassword"))
    return testo == decripted_text

def test_wrong_password():
    try:
        testo = "ciao mondo"
        encrypted = encrypt(testo, "miapassword")
        decripted_text =(decrypt(encrypted, "miapasswor"))
        print(decripted_text)
        return testo != decripted_text
    except:
        return 1

def test_salt_randomness():
    testo = "ciao mondo"
    encrypted_1 = encrypt(testo, "miapassword")
    encrypted_2 = encrypt(testo, "miapassword")
    salt_1 = encrypted_1[:16]
    salt_2 = encrypted_2[:16]
    return salt_1 != salt_2

