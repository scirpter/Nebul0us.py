from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class SPECTATE_GAME_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream().write_byte(self.packet_type.value).get_stream()
        )

        return self.stream
