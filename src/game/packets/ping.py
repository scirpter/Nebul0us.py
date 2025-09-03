from __future__ import annotations
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.models.client.client import Client


class PING(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = ByteArray().write_byte(self.packet_type).write_int(0).data()
        self.client.app.devlog(f"Ping? {self.client.client_data.name}", "info")
        return self.stream
