from __future__ import annotations
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models.client.client import Client


class CONNECT_RESULT_2(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        stream.read_byte()
        self.rng_token1 = stream.read_int()
        stream.read_byte()
        self.client.client_data.cr2_token1 = stream.read_int()
        self.client.client_data.cr2_token2 = stream.read_int()
        _strange_value = stream.read_int()
        stream.read_int()
        stream.read_float()
        stream.read_byte()
        self.client.app.notify(
            "Lobby",
            f"{self.client.client_data.name} connected",
        )
