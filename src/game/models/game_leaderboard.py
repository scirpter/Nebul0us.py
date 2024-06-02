from base.custom_types import RELATIVE_ENTITY_ID


class LeaderboardEntry:
    def __init__(self, player_entity_id: RELATIVE_ENTITY_ID, score: int) -> None:
        self.player_entity_id: RELATIVE_ENTITY_ID = player_entity_id
        self.score: int = score


class GameLeaderboard:
    def __init__(self) -> None:
        self.entries: list[LeaderboardEntry] = []
