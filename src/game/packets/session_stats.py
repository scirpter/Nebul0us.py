from __future__ import annotations
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models.client.client import Client


class SESSION_STATS(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        _id = stream.read_byte()

        if (
            self.client.options_data.auto_respawn
            and self.client.is_connected
            and (
                not (
                    (self.client.client_data.world.time_left or 32767) >= 65550
                    and (self.client.client_data.world.time_left or 32767) < 65535
                )
                or (self.client.client_data.world.time_left == 32767)
            )
        ):
            self.client.do_respawn_after_death()
