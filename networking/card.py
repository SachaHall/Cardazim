from __future__ import annotations

import os

from crypt_image import CryptImage
from typing import Union
from os import PathLike
from utils import get_str_from_bytes, encode_str


class Card:
    def __init__(self, name: str, creator: str, riddle: str,
                 solution: Union[str, None], image: CryptImage):
        self.name: str = name
        self.creator: str = creator
        self.riddle: str = riddle
        self.solution: str = solution
        self.image: CryptImage = image

    def __repr__(self):
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self):
        return f"""
        Card {self.name} by {self.creator}
        riddle: {self.riddle}
        solution {self.solution if self.solution is not None else "unsolved"}
        """

    @classmethod
    def create_from_path(cls, name: str, creator: str, path: Union[str,
    PathLike], riddle: str, solution: str):
        image = CryptImage.create_from_path(path)
        return cls(name, creator, riddle, solution, image)

    def serialize(self) -> bytes:
        name: bytes = encode_str(self.name)
        creator: bytes = encode_str(self.creator)
        riddle: bytes = encode_str(self.riddle)
        return name + creator + self.image.get_image_data() + riddle

    @classmethod
    def deserialize(cls, data: bytes) -> Card:
        name, data = get_str_from_bytes(data)
        creator, data = get_str_from_bytes(data)
        image, data = CryptImage.create_from_bytes(data)
        riddle, data = get_str_from_bytes(data)
        return Card(name, creator, riddle, None, image)


def main():
    solution = "Brakha"
    os.chdir(os.path.dirname(__file__))
    card = Card.create_from_path("Card1", "Sacha The Boss",
                                 "soldier.jpeg",
                                 "What do you say before eating?", solution)
    card.image.encrypt(card.solution)
    data = card.serialize()
    card2 = Card.deserialize(data)
    if card2.image.decrypt(solution):
        card2.solution = solution
    assert (repr(card) == repr(card2))
    card2.image.show()


if __name__ == "__main__":
    main()
