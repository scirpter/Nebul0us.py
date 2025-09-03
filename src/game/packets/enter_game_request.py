from __future__ import annotations
from typing import TYPE_CHECKING
from game.sigs import APP_VERSION_SIG
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


class ENTER_GAME_REQUEST(Packet):
    def __init__(
        self,
        client: Client,
        lobby_name: str | None = None,
        player_id: int | None = None,
    ) -> None:
        super().__init__(client, self)
        self.lobby_name: str | None = lobby_name
        self.account_id: int | None = player_id

    def write(self) -> bytes:
        self.stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.client_data.rng_token1)
            .write_int(0xFFFFFFFF)
            .write_utf(self.lobby_name or "")
            .write_int(self.account_id or -1)
            .write_byte(-1)
            .write_short(APP_VERSION_SIG)
            .data()
        )

        return self.stream
