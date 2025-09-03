from __future__ import annotations
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING
from binascii import hexlify


if TYPE_CHECKING:
    from game.models.client.client import Client


class PONG(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        stream.read_byte()
        self.client.client_data.pingpong_token = stream.read_raw(8)
        self.client.app.devlog(
            f"Pong! {self.client.client_data.name} with {hexlify(self.client.client_data.pingpong_token).decode()}",
            "info",
        )
