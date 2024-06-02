from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class EMOTE_REQUEST(Packet):
    def __init__(self, client: Client, emote_id: int) -> None:
        super().__init__(client, self)
        self.emote_id: int = emote_id

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.client_data.cr2_token1)
            .write_byte(self.emote_id)
            .write_int(self.client.client_data.rng_token1)
            .write_int(0x00000000)
            .get_stream()
        )

        return self.stream
