from enum import Enum


class Difficulty(Enum):
    (
        EASY,
        MEDIUM,
        HARD,
        IMPOSSIBLE,
    ) = range(4)
