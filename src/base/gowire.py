from socket import socket, AF_INET, SOCK_DGRAM
from binascii import hexlify, unhexlify


WIRE_PORT = 27900
TARGET_WIRE_PORT = 27901


class Gowire:
    def __init__(self) -> None:
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(("", WIRE_PORT))

    def verify(self, stream: bytes) -> bytes:
        self.sock.sendto(
            f"VERIFY({hexlify(stream).decode()})".encode(),
            ("localhost", TARGET_WIRE_PORT),
        )

        while True:
            data, _ = self.sock.recvfrom(1024)
            actual: str = data.decode()
            if actual.startswith("VERIFY("):
                return unhexlify(actual[7:-1])

    def recv(self) -> str:
        return self.sock.recv(1024).decode()
