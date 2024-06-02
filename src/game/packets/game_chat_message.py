from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class GAME_CHAT_MESSAGE(Packet):
    def __init__(self, client: Client, stream: bytes = b"", message: str = "") -> None:
        super().__init__(client, self, stream)
        self.player_name: str = ""
        self.player_account_id: int = 0
        self.message: str = message

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        stream.read_int()
        self.player_name = stream.read_utf()
        self.message = stream.read_utf()
        self.player_account_id = stream.read_int()
        stream.read_bool()
        stream.read_long()
