from game.sigs import KEEP_ALIVE_SIG

from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class KEEP_ALIVE(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.client_data.cr2_token2)
            .write_int(KEEP_ALIVE_SIG)
            .write_int(self.client.client_data.rng_token1)
            .get_stream()
        )

        return self.stream
