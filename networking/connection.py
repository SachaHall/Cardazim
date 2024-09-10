import socket
import struct
import time


class Connection:
    def __init__(self, connection: socket.socket):
        self.__connection__: socket.socket = connection

    def send_message(self, message: bytes):
        self.__connection__.send(struct.pack('<I', len(message)))
        self.__connection__.send(message)

    def receive_message(self):
        sz: int = struct.unpack("<I", self.__connection__.recv(4))[0]
        return self.__connection__.recv(sz).decode('utf-8')

    @classmethod
    def connect(cls, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        return cls(conn)

    def close(self):
        self.__connection__.close()

    def __repr__(self):
        return (
            f"connection from {self.__connection__.getsockname()}"
            f" to {self.__connection__.getpeername()}"
        )

    def get_client_name(self):
        return self.__connection__.getpeername()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    with Connection.connect('127.0.0.1', 8080) as connection:
        print(connection)
        connection.send_message(b'hello')
        data = connection.receive_message()
        print(data)


if __name__ == "__main__":
    main()
