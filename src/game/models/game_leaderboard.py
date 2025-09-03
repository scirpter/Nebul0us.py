class LeaderboardEntry:
    def __init__(self, player_entity_id: int, score: int) -> None:
        self.player_entity_id: int = player_entity_id
        self.score: int = score


class GameLeaderboard:
    def __init__(self) -> None:
        self.entries: list[LeaderboardEntry] = []

    def get_sorted_entries(self) -> list[LeaderboardEntry]:
        return sorted(self.entries, key=lambda e: e.score, reverse=True)

    def update(self, entries: list[LeaderboardEntry]) -> None:
        self.entries = entries

    def clear(self) -> None:
        self.entries.clear()
