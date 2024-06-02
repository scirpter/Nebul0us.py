from game.enums import GAME_MODE, FONT, COLOR_CYCLE
from game.models.client.client import Client
from game.natives import GET_COMMON_REQUEST_STAMP
from helpers.java_data_stream import JavaDataOutputStream

from .packet import Packet
from random import randint
from game.sigs import APP_VERSION_SIG


class CONNECT_REQUEST_3(Packet):
    def __init__(
        self,
        client: Client,
        game_mode: GAME_MODE,
        do_connect_in_private_search: bool,
        go_mayhem: bool,
        b64_auth_token: str,
    ) -> None:
        super().__init__(client, self)
        self.game_mode: GAME_MODE = game_mode
        self.do_connect_in_private_search: bool = do_connect_in_private_search
        self.go_mayhem: bool = go_mayhem
        self.b64_auth_token: str = b64_auth_token
        self.raw_stream: bytes = b""

    def write(self) -> bytes:
        u64_rnd: int = randint(0, 0xFFFFFFFFFFFFFFFF)
        stream: JavaDataOutputStream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(0x00000000)
            .write_long(u64_rnd)
            .write_short(APP_VERSION_SIG)
            .write_int(self.client.client_data.rng_token1)
            .write_byte(self.game_mode.value)
            .write_bool(self.do_connect_in_private_search)
            .write_int(0xFFFFFFFF)
            .write_utf("")
            .write_byte(self.client.client_data.profile_visibility.value)
            .write_bool(self.go_mayhem)
            .write_short(self.client.wardrobe.skin.value)
            .write_byte(0xFF)
            .write_utf(self.client.client_data.name)
            .write_int(0x00000000)
            .write_byte(len(self.client.client_data.name))
        )

        for _ in range(len(self.client.client_data.name)):
            stream.write_byte(0xFF)

        (
            stream.write_byte(0xFF)
            .write_int(self.client.client_data.rng_token2)
            .write_utf("")
            .write_byte(self.client.wardrobe.hat or 0xFF)
            .write_int(0x00000000)
            .write_byte(self.client.wardrobe.halo or 0x00)
            .write_byte(0xFF)
            .write_utf("")
            .write_int(0x00000000)
            .write_int(0x00000000)
            .write_byte(self.client.wardrobe.particle or 0xFF)
            .write_byte(
                FONT.DEFAULT.value
                if not self.client.wardrobe.name_font
                else self.client.wardrobe.name_font.value
            )
            .write_byte(0x05)
        )

        for _ in range(5):
            stream.write_byte(0x77)

        (
            stream.write_byte(
                COLOR_CYCLE.NONE.value
                if not self.client.wardrobe.color_cycle
                else self.client.wardrobe.color_cycle.value
            )
            .write_short(0x0000)
            .write_short(0x0000)
            .write_int(0x00000000)
            .write_long(GET_COMMON_REQUEST_STAMP())
            .write_short(0x0100)
            .write_fully(self.b64_auth_token.encode("utf8"))
        )

        self.raw_stream = stream.get_stream()
        self.stream = self.client.app.wire.verify(
            self.client.app.statery["license_key"], stream.get_stream()
        )

        return self.stream
