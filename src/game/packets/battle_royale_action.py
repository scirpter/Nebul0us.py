from game.models.client.client import Client
from helpers.java_data_stream import JavaDataOutputStream
from .packet import Packet


class BATTLE_ROYALE_ACTION(Packet):
    def __init__(self, client: Client, do_register: bool) -> None:
        super().__init__(client, self)
        self.do_register: bool = do_register

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.client_data.cr2_token1)
            .write_byte(0x01 if self.do_register else 0x02)
            .get_stream()
        )
        return self.stream
