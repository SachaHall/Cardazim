from __future__ import annotations
from typing import Union
import argparse
import sys
from connection import Connection
from card import Card
from os import PathLike

def send_data(server_ip: str, server_port: int, data: bytes) -> None:
    """
    Send data to server in address (server_ip, server_port).
    """
    with Connection.connect(server_ip, server_port) as connection:
        print(connection)
        connection.send_message(data)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the name')
    parser.add_argument('creator', type=str,
                        help='the creator')
    parser.add_argument('riddle', type=str,
                        help='the riddle')
    parser.add_argument('solution', type=str,
                        help='the solution to the riddle')
    parser.add_argument('path', type=Union[PathLike, str],
                        help='the path to the image')

    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    card: Card = Card.create_from_path(args.name, args.creator, args.path, args.riddle, args.solution)
    card.image.encrypt("oulala")
    send_data(args.server_ip, args.server_port, card.serialize())
    print('Done.')



if __name__ == '__main__':
    sys.exit(main())
