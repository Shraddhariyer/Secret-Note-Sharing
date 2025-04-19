from Crypto.Cipher import AES
import base64
import os
import hashlib

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode()).digest()
    raw = pad(raw)
    iv = os.urandom(16)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode()))

def decrypt(enc, password):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(hashlib.sha256(password.encode()).digest(), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]).decode('utf-8'))
