from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class SESSION_STATS(Packet):
    """When a player rejoins, this is the packet received.
    Excludes the own client.
    """

    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.cr2_token2: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.cr2_token2 = stream.read_int()
