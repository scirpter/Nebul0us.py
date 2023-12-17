from base.custom_types import ENTITY_ID
from helpers.plugins import ScriptEvent
from enums.packet_type import PACKET_TYPE
from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from packets.packet import Packet


class CLIENT_PREFERENCES(Packet):
    """Issued when a player (re)spawns"""

    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, PACKET_TYPE.CLIENT_PREFERENCES, stream)
        self.relative_entity_id: ENTITY_ID = ENTITY_ID(0)
        self.player_name: str = ""
        self.player_id: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.relative_entity_id = ENTITY_ID(stream.read_byte())
        stream.read_short()
        self.player_name = stream.read_utf()
        self.player_id = stream.read_int()

        self.client.app.dispatch(ScriptEvent.PACKET_READ, self)

    @property
    def battle_royale_register_count(self) -> int:
        """Updates slowly. May be inaccurate if players are joining too fast"""
        return self.__battle_royale_register_count

    @battle_royale_register_count.setter
    def battle_royale_register_count(self, value: int) -> None:
        self.__battle_royale_register_count = value
