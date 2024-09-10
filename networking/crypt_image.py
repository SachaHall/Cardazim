from __future__ import annotations
from os import PathLike
from typing import Union
from PIL import Image


class CryptImage:
    def __init__(self, image, key):
        self.image: Image = image
        self.key = key

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> CryptImage:

