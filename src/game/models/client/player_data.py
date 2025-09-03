from __future__ import annotations
from typing import TYPE_CHECKING

from game.models.point import Point


if TYPE_CHECKING:
    from game.models.client.client import Client


class PlayerData:
    def __init__(self, client: Client) -> None:
        self.__client: Client = client
        self.fast_local_mass: float | None = None
        self.recombine_time: float | None = None

    def get_local_avg_pos(self) -> Point | None:
        player = self.__client.client_data.world.get_player_by_name(
            self.__client.client_data.name
        )
        if not player:
            return None

        return player.get_avg_pos()
