from __future__ import annotations
from typing import TYPE_CHECKING
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


class DISCONNECT(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.client_data.cr2_token2)
            .write_int(self.client.client_data.rng_token1)
            .data()
        )

        return self.stream
