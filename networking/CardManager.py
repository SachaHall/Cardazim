from __future__ import annotations
from typing import Union
from card import Card
from os import PathLike
import os
from pathlib import Path
import json


class CardManager:
    def get_identifier(self, card: Card) -> str:
        return card.get_identifier()

    def save(self, card: Card, dir_path: Union[str, PathLike] = '.'):
        path = os.path.join(dir_path, self.get_identifier(card))
        Path(path).mkdir(parents=True, exist_ok=True)
        os.chdir(path)
        image_path = os.path.join(path, "image.png")
        open(image_path, "w")
        card.image.image.save(image_path)
        json_content = {"card.name": card.name,
                        "card.creator": card.creator,
                        "card.riddle": card.riddle,
                        "card.solution": card.solution,
                        "image_path": image_path}
        json_obj = json.dumps(json_content)
        with open("metadata.json", "w") as f:
            f.write(json_obj)

