from game.enums import GAME_MODE, WORLD_SIZE, DIFFICULTY, SPLIT_MULTIPLIER
from game.models.dot import Dot
from game.models.ejection import Ejection
from game.models.game_leaderboard import GameLeaderboard
from game.models.hole import Hole
from game.models.io import UndefinedIo
from game.models.item import Item
from game.models.jo import UndefinedJo
from game.models.m0 import UndefinedM0
from game.models.player import Player
from game.models.r0 import UndefinedR0
from game.models.spell import Spell
from game.models.wall import Wall


class World:
    def __init__(self) -> None:
        self.name: str | None = None
        self.time_left: int | None = None
        self.game_mode: GAME_MODE | None = None
        self.max_players: int | None = None
        self.spectator_count: int | None = None
        self.tick: int | None = None
        self.control_tick: int | None = None
        self.raw_size: float | None = None
        self.size: WORLD_SIZE | None = None
        self.token: int | None = None
        self.id_: int | None = None

        self.ejections: dict[int, Ejection] = {}
        self.players: dict[int, Player] = {}
        self.dots: dict[int, Dot] = {}
        self.items: dict[int, Item] = {}
        self.spells: dict[int, Spell] = {}
        self.holes: dict[int, Hole] = {}
        self.ios: dict[int, UndefinedIo] = {}
        self.jos: dict[int, UndefinedJo] = {}
        self.r0s: dict[int, UndefinedR0] = {}
        self.walls: dict[int, Wall] = {}
        self.m0s: dict[int, UndefinedM0] = {}

        self.leaderboard = GameLeaderboard()

    def get_player_by_name(self, name: str) -> Player | None:
        for player in self.players.values():
            if player.name.lower() == name.lower():
                return player
        return None

    def reset(self) -> None:
        self.name = None
        self.time_left = None
        self.game_mode = None
        self.max_players = None
        self.spectator_count = None
        self.control_tick = None
        self.tick = None
        self.raw_size = None
        self.size = None
        self.token = None
        self.id_ = None

        self.leaderboard.clear()
        self.ejections.clear()
        self.players.clear()
        self.dots.clear()
        self.items.clear()
        self.spells.clear()
        self.holes.clear()
        self.r0s.clear()
        self.ios.clear()
        self.jos.clear()
        self.walls.clear()
        self.m0s.clear()


class WorldCreatorProps:
    def __init__(
        self,
        *,
        is_hidden: bool,
        min_players: int,
        max_players: int,
        game_mode: GAME_MODE,
        size: WORLD_SIZE,
        difficulty: DIFFICULTY,
        name: str,
        duration_minutes: int | None,
        is_mayhem: bool,
        split_multiplier: SPLIT_MULTIPLIER,
        allow_ultra_click: bool,
        allow_mass_boost: bool,
        allow_rainbow_holes: bool,
        wall_count: int,
        allow_admin: bool,
        allow_guests: bool,
        is_arena: bool,
    ) -> None:
        self.is_hidden: bool = is_hidden
        self.min_players: int = min_players
        self.max_players: int = max_players
        self.game_mode: GAME_MODE = game_mode
        self.size: WORLD_SIZE = size
        self.difficulty: DIFFICULTY = difficulty
        self.name: str = name
        self.duration_minutes: int | None = duration_minutes
        self.is_mayhem: bool = is_mayhem
        self.split_multiplier: SPLIT_MULTIPLIER = split_multiplier
        self.allow_ultra_click: bool = allow_ultra_click
        self.allow_mass_boost: bool = allow_mass_boost
        self.allow_rainbow_holes: bool = allow_rainbow_holes
        self.wall_count: int = wall_count
        self.allow_admin: bool = allow_admin
        self.allow_guests: bool = allow_guests
        self.is_arena: bool = is_arena
