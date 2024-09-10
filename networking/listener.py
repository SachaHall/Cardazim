import socket
import threading
from connection import Connection


class Listener:
    def __init__(self, port, host, backlog=1000):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind((host, port))
        self.backlog: int = backlog

    def start(self):
        self.serv.listen(self.backlog)

    def accept(self):
        return Connection(self.serv.accept()[0])

    def stop(self):
        self.serv.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

printing_lock: threading.Lock = threading.Lock()


def run_connection(connection: Connection):
    with connection as connection:
        with printing_lock:
            print(connection.receive_message())


def main():
    with Listener(8080, '127.0.0.1') as listener:
        listener.start()
        while True:
            t: threading.Thread = threading.Thread(
                target=run_connection(listener.accept()))
            t.start()

if __name__ == "__main__":
    main()