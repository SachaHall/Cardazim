from __future__ import annotations

import os.path
from os import PathLike
from typing import Union
from PIL import Image
from hashlib import sha256
from Crypto.Cipher import AES
from utils import pack_int, unpack_int


class CryptImage:
    def __init__(self, image, key_hash):
        self.image: Image.Image = image
        self.key_hash: bytes = key_hash

    def encrypt(self, key: str) -> None:
        data: bytes = self.image.tobytes()
        size = self.image.size
        self.key_hash: bytes = sha256(sha256(key.encode()).digest()).digest()
        cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_EAX, nonce=b'arazim')
        encrypted = cipher.encrypt(data)
        try:
            assert len(encrypted) == len(data)
        except AssertionError:
            print("problem with encryption boom boom boom")
        self.image = Image.frombytes(self.image.mode, size, encrypted)

    def decrypt(self, key: str) -> bool:
        if sha256(sha256(key.encode()).digest()).digest() != self.key_hash:
            return False
        data = self.image.tobytes()
        size = self.image.size
        cipher = AES.new(sha256(key.encode()).digest(), AES.MODE_EAX, nonce=b'arazim')
        decrypted = cipher.decrypt(data)
        try:
            assert len(decrypted) == len(data)
        except AssertionError:
            print("problem with decryption boom boom boom")
        self.image = Image.frombytes(self.image.mode, size, decrypted)
        return True

    def get_image_data(self) -> bytes:
        width, height = self.image.size
        height_b: bytes = pack_int(height)
        width_b: bytes = pack_int(width)
        assert self.key_hash is not None
        a = self.image.tobytes()
        return height_b+width_b+self.image.tobytes()+self.key_hash

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> CryptImage:
        return cls(Image.open(path), None)

    @classmethod
    def create_from_bytes(cls, data: bytes) -> tuple[CryptImage, bytes]:
        uint_size = 4
        height: int = unpack_int(data[0:uint_size])
        width: int = unpack_int(data[uint_size: 2*uint_size])
        ind: int = 2*uint_size
        bin_data: bytes = data[ind: ind+3*height*width]
        ind += 3*height*width
        key_hash: bytes = data[ind:ind+32]
        image_obj: Image = Image.frombytes("RGB", (width, height), bin_data)
        image: CryptImage = CryptImage(image_obj, key_hash)
        return image, data[ind+32:]

    def show(self):
        self.image.show()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    im = CryptImage.create_from_path("soldier.jpeg")
    im.encrypt("heyo")
    im.decrypt("heyo")
