from helpers.plugins import ScriptEvent
from enums.packet_type import PACKET_TYPE
from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from packets.packet import Packet


class BATTLE_ROYALE_STATUS_UPDATE(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, PACKET_TYPE.BATTLE_ROYALE_STATUS_UPDATE, stream)
        self.__battle_royale_register_count: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        stream.read_byte()
        self.__battle_royale_register_count: int = stream.read_byte()
        self.client.app.dispatch(ScriptEvent.PACKET_READ, self)

    @property
    def battle_royale_register_count(self) -> int:
        """Updates slowly. May be inaccurate if players are joining too fast"""
        return self.__battle_royale_register_count

    @battle_royale_register_count.setter
    def battle_royale_register_count(self, value: int) -> None:
        self.__battle_royale_register_count = value
