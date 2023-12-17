from game.enums import CLAN_RANK
from helpers.plugins import ScriptEvent
from enums.packet_type import PACKET_TYPE
from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from packets.packet import Packet


class CLAN_CHAT(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, PACKET_TYPE.CLAN_CHAT_MESSAGE, stream)
        self.player_name: str = ""
        self.message: str = ""
        self.player_clan_rank: CLAN_RANK = CLAN_RANK.INVALID
        self.player_account_id: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        stream.read_int()
        self.player_name = stream.read_utf()
        self.message = stream.read_utf()

        read_byte: int = (
            stream.read_byte()
        )  # ? always writes 0? (ref c6500n1.writeByte(0);)
        enum_clan_rank_length: int = len(CLAN_RANK)
        if read_byte <= 0 or read_byte >= enum_clan_rank_length:
            self.player_clan_rank = CLAN_RANK.INVALID
        self.player_clan_rank = CLAN_RANK(read_byte)
        self.player_account_id = stream.read_int()

        if stream.space_left() > 0:
            stream.read_int()

        if stream.space_left() > 0:
            stream.read_bool()

        self.client.app.dispatch(ScriptEvent.PACKET_READ, self)

    @property
    def battle_royale_register_count(self) -> int:
        """Updates slowly. May be inaccurate if players are joining too fast"""
        return self.__battle_royale_register_count

    @battle_royale_register_count.setter
    def battle_royale_register_count(self, value: int) -> None:
        self.__battle_royale_register_count = value
