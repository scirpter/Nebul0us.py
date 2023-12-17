from enums.packet_type import PACKET_TYPE
from game.models.client.client import Client
from abc import ABC, abstractmethod


class Packet(ABC):
    @abstractmethod
    def __init__(
        self, client: Client, packet_type: PACKET_TYPE, stream: bytes = b""
    ) -> None:
        self.client: Client = client
        self.packet_type: PACKET_TYPE = packet_type
        self.stream: bytes = stream
