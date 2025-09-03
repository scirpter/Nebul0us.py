from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from game.enums.packet_type import PACKET_TYPE


if TYPE_CHECKING:
    from game.models.client.client import Client


class Packet(ABC):
    @abstractmethod
    def __init__(self, client: Client, packet_cls: Packet, stream: bytes = b"") -> None:
        self.client: Client = client
        self.packet_type: int = (
            0
            if not PACKET_TYPE.get_type_from_str(packet_cls.__class__.__name__)
            else PACKET_TYPE.get_type_from_str(packet_cls.__class__.__name__).value
        )
        self.stream: bytes = stream

    def write(self) -> bytes:
        return self.stream

    def zero(self) -> bytes:
        return b"\x00"
