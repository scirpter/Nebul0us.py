from socket import socket, AF_INET, SOCK_DGRAM
from threading import Lock


WIRE_PORT = 27900
TARGET_WIRE_PORT = 27901


class Gowire:
    def __init__(self) -> None:
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(("", WIRE_PORT))
        self.verify_lock = Lock()

    def verify(self, license_key: str, connect_request_stream: bytes) -> bytes:
        with self.verify_lock:
            self.sock.sendto(
                f"VERIFY::{connect_request_stream.decode()}::{license_key}".encode(),
                ("localhost", TARGET_WIRE_PORT),
            )

            data, _ = self.sock.recvfrom(1024)
            return data

    def recv(self) -> str:
        return self.sock.recv(1024).decode()
