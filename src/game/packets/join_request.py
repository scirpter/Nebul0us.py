from __future__ import annotations
from typing import TYPE_CHECKING
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


class JOIN_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        xlen = 5
        self.stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_short(self.client.wardrobe.skin.value)
            .write_utf(self.client.client_data.name)
            .write_byte(0xFF)
            .write_int(0)
            .write_byte(len(self.client.client_data.name))
            .write_raw(b"\xff" * len(self.client.client_data.name))
            .write_byte(0xFF)
            .write_int(self.client.client_data.rng_token2)
            .write_utf("")  # pet name 1?
            .write_byte(self.client.wardrobe.hat or 0xFF)
            .write_int(0)
            .write_byte(self.client.wardrobe.halo or 0)
            .write_byte(0xFF)
            .write_utf("")  # pet name 2?
            .write_int(0)
            .write_int(0)
            .write_byte(self.client.wardrobe.particle or 0)
            .write_byte(self.client.wardrobe.name_font.value)
            .write_byte(xlen)
            .write_byte(self.client.wardrobe.color_cycle.value)
            .write_short(0)
            .write_int(0)
            .write_short(0)  # actually native function but is always 0
            .write_int(0)
            .write_int(self.client.client_data.rng_token1)
            .write_raw(b"\x77" * xlen)
            .data()
        )

        return self.stream
