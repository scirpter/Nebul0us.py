from game.enums.game_mode import GAME_MODE
from game.enums.split_multiplier import SPLIT_MULTIPLIER
from game.enums.world_size import WORLD_SIZE


class SearchListEntry:
    def __init__(
        self,
        *,
        room_id: int,
        name: str,
        game_mode: GAME_MODE,
        game_size: WORLD_SIZE,
        max_players: int,
        players_in_lobby: int,
        host_name: str,
        host_account_id: int,
        split_multiplier: SPLIT_MULTIPLIER,
        allow_mass_boost: bool,
    ) -> None:
        self.room_id = room_id
        self.name = name
        self.game_mode = game_mode
        self.game_size = game_size
        self.players_in_lobby = players_in_lobby
        self.max_players = max_players
        self.host_name = host_name
        self.host_account_id = host_account_id
        self.split_multiplier = split_multiplier
        self.allow_mass_boost = allow_mass_boost


class PrivateSearchList:
    def __init__(self) -> None:
        self.token = 0
        self.entries: list[SearchListEntry] = []
        self.results_per_page: int = 20
        self.page: int = 0

    def reset(self) -> None:
        self.token = 0
        self.entries.clear()
