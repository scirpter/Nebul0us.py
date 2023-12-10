from socket import socket, AF_INET, SOCK_DGRAM


WIRE_PORT = 27900
TARGET_WIRE_PORT = 27901


class Gowire:
    def __init__(self) -> None:
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(("", WIRE_PORT))

    def verify(self, data: str) -> None:
        self.sock.sendto(f"VERIFY({data})".encode(), ("localhost", TARGET_WIRE_PORT))

    def recv(self) -> str:
        return self.sock.recv(1024).decode()
