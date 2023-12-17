from game.enums import GAME_MODE, WORLD_SIZE, DIFFICULTY, SPLIT_MULTIPLIER
from game.models.dot import Dot
from game.models.ejection import Ejection
from game.models.hole import Hole
from game.models.item import Item
from game.models.player import Player
from game.models.spell import Spell


class World:
    name: str | None
    time_left: int | None
    game_mode: GAME_MODE | None
    max_players: int | None
    spectator_count: int | None
    tick: int | None
    raw_size: float | None
    size: WORLD_SIZE | None
    token: int | None

    ejections: dict[int, Ejection] = {}
    players: dict[int, Player] = {}
    dots: dict[int, Dot] = {}
    items: dict[int, Item] = {}
    spells: dict[int, Spell] = {}
    holes: dict[int, Hole] = {}

    def reset(self) -> None:
        self.name = None
        self.time_left = None
        self.game_mode = None
        self.max_players = None
        self.spectator_count = None
        self.tick = None
        self.raw_size = None
        self.size = None
        self.token = None

        self.ejections.clear()
        self.players.clear()
        self.dots.clear()
        self.items.clear()
        self.spells.clear()
        self.holes.clear()


class WorldProps:
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
