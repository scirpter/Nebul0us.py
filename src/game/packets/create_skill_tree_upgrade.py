from __future__ import annotations
import base64
from typing import TYPE_CHECKING
from game.enums.rpg_skilltree import RPG_SKILLTREE_UPGRADE
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


class CREATE_SKILL_TREE_UPGRADE(Packet):
    def __init__(
        self,
        client: Client,
        upgrade: RPG_SKILLTREE_UPGRADE,
        reset_token: str | None = None,
    ) -> None:
        super().__init__(client, self)
        self.reset_token = reset_token  # ? api request, not needed for now, but request is implemented
        self.upgrade = upgrade

    def write(self) -> bytes:
        do_upgrades_reset = self.reset_token is not None
        z6 = True
        stream = (
            ByteArray()
            .write_byte(self.packet_type)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.client_data.rng_token1)
            .write_bool(do_upgrades_reset)
        )

        if do_upgrades_reset and self.reset_token:
            stream.write_short(len(self.reset_token))
            stream.write_raw(base64.b64decode(self.reset_token))
        else:
            stream.write_byte(self.upgrade.value)

        stream.write_bool(z6)  # ? idk what z6 is

        self.stream = stream.data()
        return self.stream
