import socket
import struct
import time


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection: socket.socket = connection

    def send_message(self, message: bytes):
        self.connection.send(struct.pack('<I', len(message)))
        self.connection.send(message)

    def receive_message(self):
        sz: int = struct.unpack("<I", self.connection.recv(4))[0]
        time.sleep(1)
        return self.connection.recv(sz).decode('utf-8')

    @classmethod
    def connect(cls, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        return cls(conn)

    def close(self):
        self.connection.close()

    def __repr__(self):
        return (
            f"connection from {self.connection.getsockname()}"
            f" to {self.connection.getpeername()}"
        )

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
