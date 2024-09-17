from Crypto.Cipher import AES
import hashlib
key = b'Sixtfrfrfreen byte keyde'
en_key = hashlib.sha256(key).digest()
plaintext = b'hello worljjjjfd'
cipher = AES.new(en_key, AES.MODE_EAX, nonce=b'arazim')
encrypted = cipher.encrypt(plaintext)
print(len(encrypted) == len(plaintext))