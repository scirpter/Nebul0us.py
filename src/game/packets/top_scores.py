from typing import Any
from base.custom_types import RELATIVE_ENTITY_ID
from game.enums.game_mode import GAME_MODE
from game.enums.world_size import WORLD_SIZE
from game.models.game_leaderboard import GameLeaderboard, LeaderboardEntry
from game.natives import RNATIVE_LE_SHORT_INT

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


LEADERBOARD_COUNT = 5


class TOP_SCORES(Packet):
    """When a player rejoins, this is the packet received.
    Excludes the own client.
    """

    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.world_name: str = ""
        self.world_token: int = 0
        self.time_left: int = 0
        self.game_mode: GAME_MODE = GAME_MODE(0)
        self.world_size: WORLD_SIZE = WORLD_SIZE(0)
        self.max_player_count: int = 0
        self.player_count: int = 0
        self.spectator_count: int = 0

        self.js: dict[RELATIVE_ENTITY_ID, dict[str, Any]] = {}
        self.leaderboard: GameLeaderboard = GameLeaderboard()

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.world_name = stream.read_utf()
        self.world_token = stream.read_int()
        self.time_left = stream.read_short()
        self.game_mode = GAME_MODE(stream.read_byte())
        self.world_size = WORLD_SIZE((stream.read_byte() & 12) >> 2)
        self.max_player_count = stream.read_byte()
        self.player_count = stream.read_byte()

        for _ in range(self.player_count):
            entity_id = RELATIVE_ENTITY_ID(0)
            j: int = stream.read_short()
            ii = 0
            fluct_net_id = RELATIVE_ENTITY_ID(stream.read_byte())
            if self.game_mode == GAME_MODE.BATTLE_ROYALE:
                entity_id = fluct_net_id
                ii = -1
            else:
                entity_id: RELATIVE_ENTITY_ID = RELATIVE_ENTITY_ID(fluct_net_id & 31)

            self.js[entity_id] = {"j": j, "ii": ii, "fluct_net_id": fluct_net_id}

        for _ in range(LEADERBOARD_COUNT):
            entity_id = RELATIVE_ENTITY_ID(stream.read_byte())  # 255 if no player
            score: int = RNATIVE_LE_SHORT_INT(stream)
            self.leaderboard.entries.append(LeaderboardEntry(entity_id, score))

        all_data: bytes = stream.get_stream()
        self.spectator_count = all_data[len(all_data) - 13] // 2
