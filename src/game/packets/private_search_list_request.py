from __future__ import annotations
from typing import TYPE_CHECKING
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


class PRIVATE_SEARCH_LIST_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_short(
                self.client.private_search_list.page
                * self.client.private_search_list.results_per_page
            )
            .write_byte(self.client.private_search_list.results_per_page)
            .write_byte(0x02)
            # filters
            .write_byte(-1)  # game mode
            .write_byte(-1)  # ..the rest no idea, game size etc
            .write_byte(-1)
            .write_byte(-1)
            .write_byte(-1)
            .write_byte(-1)
            .write_byte(-1)
            .write_byte(-1)
            .write_bool(False)  # no idea
            .write_int(self.client.client_data.rng_token1)
            .write_byte(-1)  # or 0 or 1, bool dependant
            .data()
        )
        return self.stream
