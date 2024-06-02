from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class JOIN_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, self)

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.wardrobe.skin.value)
            .write_utf(self.client.client_data.name)
            .write_short(0xFF00)
            .write_int(len(self.client.client_data.name))
            .write_short(0xFFFF)
            .write_fully(("ff" * len(self.client.client_data.name)).encode())
            .write_fully(b"e1d452")
            .write_utf("")
            .write_byte(self.client.wardrobe.hat or 0xFF)
            .write_int(0x00000000)
            .write_byte(self.client.wardrobe.halo or 0x00)
            .write_byte(0xFF)
            .write_utf("")
            .write_int(0x00000000)
            .write_int(0x00000000)
            .write_byte(self.client.wardrobe.particle or 0xFF)
            .write_byte(self.client.wardrobe.name_font.value)
            .write_byte(0x05)
            .write_byte(self.client.wardrobe.color_cycle.value)
            .write_short(0x0000)
            .write_int(0x00000000)
            .write_short(0x0000)
            .write_int(0x00000000)
            .write_int(self.client.client_data.rng_token1)
            .write_fully(b"7777777777")
            .get_stream()
        )

        return self.stream
