import pytest
import sys
import struct
import os
import sys
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'networking')))
from connection import Connection
from card import Card
import client as cl
import socket
from crypt_image import CryptImage

class MockSocket:
    sent_data = []
    addr = None

    def __init__(self, connection):
        self.__connection__ = connection

    @classmethod
    def connect(cls, host, port):
        MockSocket.addr = (host, port)
        return cls(None)

    def send_message(self, data: bytes):
        MockSocket.sent_data.append(data)

    def close(self):
        pass

    def get_client_name(self):
        pass

    def __repr__(self):
        return ("connection very yes yes beautiful")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_connection(monkeypatch):
    monkeypatch.setattr('client.Connection', MockSocket)


def test_run_client(mock_connection):
    os.chdir(os.path.dirname(__file__))
    sys.argv = ["oulala"]
    sys.argv.append("127.0.0.1")
    sys.argv.append("8080")
    sys.argv.append("super_card")
    sys.argv.append("sacha")
    sys.argv.append("Who let the dogs out?")
    sys.argv.append("Who")
    sys.argv.append(
        "../networking/grimace.jpeg")
    cl.main()

    assert MockSocket.addr == ('127.0.0.1', 8080)
    card = Card.deserialize(MockSocket.sent_data[0])
    assert card.name == "super_card"
    assert card.creator == "sacha"
    assert card.riddle == "Who let the dogs out?"
    os.chdir(os.path.dirname(__file__))
    assert card.image.decrypt("Who")
    card.image.show()
    assert card.image.image.tobytes() == CryptImage.create_from_path("../networking/grimace.jpeg").image.tobytes()

