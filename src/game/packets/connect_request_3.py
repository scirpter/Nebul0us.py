from __future__ import annotations
from game.enums import GAME_MODE, FONT, COLOR_CYCLE
from typing import TYPE_CHECKING
from game.natives import GET_REQUEST_TS
from helpers._io.bytearray import ByteArray
from .packet import Packet
from game.sigs import APP_VERSION_SIG
import base64


if TYPE_CHECKING:
    from game.models.client.client import Client


class CONNECT_REQUEST_3(Packet):
    def __init__(
        self,
        client: Client,
        game_mode: GAME_MODE,
        do_connect_in_private_search: bool,
        is_mayhem: bool,
        b64_auth_token: str,
        pingpong_token: bytes,
        auth_nonce: int,
    ) -> None:
        super().__init__(client, self)
        self.game_mode: GAME_MODE = game_mode
        self.do_connect_in_private_search: bool = do_connect_in_private_search
        self.is_mayhem: bool = is_mayhem
        self.b64_auth_token: str = b64_auth_token
        self.pingpong_token: bytes = pingpong_token
        self.auth_nonce: int = auth_nonce

    def write(self) -> bytes:
        stream: ByteArray = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.auth_nonce)
            .write_byte(8)  # length of pingpong_token
            .write_raw(self.pingpong_token)
            .write_short(APP_VERSION_SIG)
            .write_int(self.client.client_data.rng_token1)
            .write_byte(self.game_mode.value)
            .write_bool(self.do_connect_in_private_search)
            .write_int(-1)
            .write_byte(self.client.client_data.profile_visibility.value)
            .write_bool(self.is_mayhem)
            .write_short(self.client.wardrobe.skin.value)
            .write_byte(self.client.wardrobe.eject_skin or -1)
            .write_utf(self.client.client_data.name)
            .write_int(0)
            .write_byte(len(self.client.client_data.name))
        )

        for _ in range(len(self.client.client_data.name)):
            stream.write_byte(-1)

        (
            stream.write_byte(-1)
            .write_int(self.client.client_data.rng_token2)
            .write_utf("")
            .write_byte(self.client.wardrobe.hat or -1)
            .write_int(0)
            .write_byte(self.client.wardrobe.halo or 0)
            .write_byte(-1)
            .write_utf("")
            .write_int(0)
            .write_int(0)
            .write_byte(self.client.wardrobe.particle or -1)
            .write_byte(
                FONT.DEFAULT.value
                if not self.client.wardrobe.name_font
                else self.client.wardrobe.name_font.value
            )
            .write_byte(5)
        )

        for _ in range(5):
            stream.write_byte(0x77)

        (
            stream.write_byte(
                COLOR_CYCLE.NONE.value
                if not self.client.wardrobe.color_cycle
                else self.client.wardrobe.color_cycle.value
            )
            .write_short(0)
            .write_short(0)
            .write_int(0)
            .write_long(GET_REQUEST_TS())
            .write_short(0x0100)
            .write_raw(base64.b64decode(self.b64_auth_token))
        )

        self.stream = stream.data()
        return self.stream
