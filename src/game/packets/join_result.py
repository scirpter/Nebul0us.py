from base.custom_types import RELATIVE_ENTITY_ID

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class JOIN_RESULT(Packet):
    """When a player rejoins, this is the packet received.
    Excludes the own client.
    """

    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.cr2_token2: int = 0
        self.entity_id: RELATIVE_ENTITY_ID = RELATIVE_ENTITY_ID(0)
        self.player_name: str = ""
        self.player_id: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.cr2_token2 = stream.read_int()
        rb = stream.read_byte()
        if rb != 0:
            return  # invalid packet

        self.entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
        stream.read_short()
        stream.read_int()  # token?
        stream.read_byte()
        self.player_name = stream.read_utf()
        self.player_id = stream.read_int()
