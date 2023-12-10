from enums.packet_type import PacketType
from game.models.client.client import Client


class Packet:
    def __init__(
        self, client: Client, packet_type: PacketType, data: bytes = b""
    ) -> None:
        self.client: Client = client
        self.packet_type: PacketType = packet_type
        self.data: bytes = data
