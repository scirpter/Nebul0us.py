from __future__ import annotations
from game.enums import PROFILE_VISIBILITY
from game.models.world import World
from helpers.common import generate_safe_int32
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.models.client.client import Client


class ClientData:
    def __init__(self, client: Client) -> None:
        self.__client: Client = client

        self.name: str = self.__client.settings["player_name"]
        self.login_ticket: str = self.__client.settings["login_ticket"]
        self.uid: int = self.__client.settings["client_uid"]
        self.server_ip: str | None = None
        self.server_port: int | None = None
        self.profile_visibility: PROFILE_VISIBILITY = (
            PROFILE_VISIBILITY.get_type_from_str(
                self.__client.settings["profile_visibility"]
            )
        )
        self.world: World = World()

        self.cr2_token1: int = 0
        self.cr2_token2: int = 0

        self.rng_token1: int = generate_safe_int32()
        self.rng_token2: int = generate_safe_int32()

        self.pingpong_token: bytes = b""

    def reset_all_tokens(self) -> None:
        self.cr2_token1 = 0
        self.cr2_token2 = 0
        self.rng_token1 = generate_safe_int32()
        self.rng_token2 = generate_safe_int32()
        self.pingpong_token = b""

    def cr_tokens_present(self) -> bool:
        return self.cr2_token1 != 0 and self.cr2_token2 != 0
