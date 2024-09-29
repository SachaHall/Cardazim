import argparse
import sys
import threading
import os
from connection import Connection
from listener import Listener
from card import Card
from CardManager import CardManager
printing_lock: threading.Lock = threading.Lock()


def run_connection(connection: Connection, dir_path: str) -> None:
    manager = CardManager()
    with connection as conn:
        data: bytes = conn.receive_message()
        print(len(data))
        card: Card = Card.deserialize(data)
        with printing_lock:
            #os.system(f"say {data}")
            print(
                f"received card: {card.name} created by {card.creator} ",
                f"from {conn.get_client_name()}")
            key = input(card.riddle)
            print(card.image.decrypt(key))
            manager.save(card, dir_path)
            card.image.show()


def run_server(ip: str, port: int, dir_path: str):
    """
    The function runs the server
    :param ip: the ip address to bind to
    :type ip: str
    :param port: the port to bind to
    :type ip: str
    """
    with Listener(port, ip) as listener:
        while True:
            t: threading.Thread = threading.Thread(
                target=run_connection(listener.accept(),dir_path))
            t.start()


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('dir_path', type=str,
                        help='the path to the database directory')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    """try:"""
    run_server(args.server_ip, args.server_port, args.dir_path)
    print('Done.')
    """except Exception as error:
        print(f'ERROR: {error}')
        return 1"""


if __name__ == '__main__':
    sys.exit(main())