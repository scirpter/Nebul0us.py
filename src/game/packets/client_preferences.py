from base.custom_types import RELATIVE_ENTITY_ID

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class CLIENT_PREFERENCES(Packet):
    """Issued when a player (re)spawns"""

    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.relative_entity_id: RELATIVE_ENTITY_ID = RELATIVE_ENTITY_ID(0)
        self.player_name: str = ""
        self.player_id: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.relative_entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
        stream.read_short()
        self.player_name = stream.read_utf()
        self.player_id = stream.read_int()

    @property
    def battle_royale_register_count(self) -> int:
        """Updates slowly. May be inaccurate if players are joining too fast"""
        return self.__battle_royale_register_count

    @battle_royale_register_count.setter
    def battle_royale_register_count(self, value: int) -> None:
        self.__battle_royale_register_count = value
