import socket
import struct
import argparse
import sys
import threading

printing_lock: threading.Lock = threading.Lock()


def run_connection(connection) -> None:
    """
    The function manages a connection with a client
    :param connection: the connection
    :rtype: None
    """
    sz: int = struct.unpack("<I", connection.recv(4))[0]
    data: bytes = connection.recv(sz)
    with printing_lock:
        print(data.decode('utf-8'))


def run_server(ip, port):
    """
    The function runs the server
    :param ip: the ip address to bind to
    :type ip: str
    :param port: the port to bind to
    :type ip: str
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
        serv.bind((ip, port))
        serv.listen()
        while True:
            connection, addr = serv.accept()
            t: threading.Thread = threading.Thread(target=run_connection(connection))
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
