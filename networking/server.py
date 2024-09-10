import argparse
import sys
import threading
import os
from connection import Connection
from listener import Listener

printing_lock: threading.Lock = threading.Lock()


def run_connection(connection: Connection) -> None:
    with connection as conn:
        data = conn.receive_message()
        with printing_lock:
            #os.system(f"say {data}")
            print(
                f"received: {data}",
                f"from {conn.get_client_name()}")


def run_server(ip: str, port: int):
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
                target=run_connection(listener.accept()))
            t.start()


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
