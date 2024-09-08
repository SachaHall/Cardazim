import socket
import struct
import argparse
import sys
import pyttsx3

def run_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
        serv.bind((ip, port))
        serv.listen()
        while True:
            connection, addr = serv.accept()
            sz = struct.unpack("<I", connection.recv(4))
            data = connection.recv(sz[0])
            print(data.decode('utf-8'))


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
    engine = pyttsx3.init()
    engine.say("hello ben the programmer")
    engine.runAndWait()
    sys.exit(main())
