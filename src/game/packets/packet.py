from __future__ import annotations
from game.enums.packet_type import PACKET_TYPE
from game.models.client.client import Client
from abc import ABC, abstractmethod


cached_packets: dict[str, PACKET_TYPE] = {}


class Packet(ABC):
    @abstractmethod
    def __init__(self, client: Client, packet_cls: Packet, stream: bytes = b"") -> None:
        self.client: Client = client
        if not cached_packets.get(packet_cls.__class__.__name__):
            cached_packets[packet_cls.__class__.__name__] = (
                PACKET_TYPE.get_type_from_str(packet_cls.__class__.__name__)
            )
        self.packet_type: PACKET_TYPE = cached_packets[packet_cls.__class__.__name__]
        self.stream: bytes = stream
