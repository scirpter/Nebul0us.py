from __future__ import annotations
import math
from random import choice
from game.natives import NATIVE_GET_CONTROL_ANGLE
from typing import TYPE_CHECKING
from helpers._io.bytearray import ByteArray
from .packet import Packet


if TYPE_CHECKING:
    from game.models.client.client import Client


class CONTROL(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        pi2: float = math.pi * 2
        angle: int = round(
            NATIVE_GET_CONTROL_ANGLE(self.client.control_data.angle, pi2)
        )
        speed: int = round(self.client.control_data.speed * 0xFF)

        stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_short(angle)
            .write_byte(speed)
            .write_byte(self.client.control_data.tick)
        )
        self.client.control_data.tick = (self.client.control_data.tick + 1) % 256
        button: int = 0
        if self.client.control_data.tick % 4 == 0:
            if self.client.control_data.do_split:
                button |= 0x01
                self.client.control_data.do_split = False
            if (
                self.client.control_data.do_eject
                or self.client.control_data.do_item_use
            ):
                button |= 0x02
                self.client.control_data.do_eject = False
            if self.client.control_data.do_item_drop:
                button |= 0x08
                self.client.control_data.do_item_drop = False

        stream.write_byte(button)

        arr: tuple[int] = (0x02, 0x0C, 0x00, 0x07, 0xFF, 0x09, 0x03, 0x01, 0x05, 0x04)  # type: ignore
        idk_id: int = choice(arr)
        stream.write_byte(idk_id)
        stream.write_int(self.client.client_data.rng_token1)
        stream.write_int(0x63)

        self.stream = stream.data()
        return self.stream
