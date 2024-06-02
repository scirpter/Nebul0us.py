from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class GROUP_LOBBY_CREATE_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            # .write_byte(self.packet_type.value)
            # .write_int(self.client.client_data.cr2_token1)
            # .write_bool()
            # .write_byte()
            # .write_byte()
            # .write_byte()  # GAME MODE
            # .write_byte(3)  # ? const?
            # .write_byte()  # DIFFICULTY
            # .write_byte()
            # .write_utf()
            # .write_utf()  # ! PLAYER NAME OF CREATOR (can be spoofed?)
            # .write_float(15.65)
            # .write_short()
            # .write_short()
            # .write_bool()
            # .write_byte()
            # .write_fully()
            # .write_byte(0x17)  # AMOUNT OF ITEMS AVAILABLE
            # # ...
            .get_stream()
        )

        return self.stream
