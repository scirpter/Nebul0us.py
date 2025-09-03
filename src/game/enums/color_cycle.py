from enum import Enum


class COLOR_CYCLE(Enum):
    (
        NONE,
        COLOR_CYCLE_SLOW,
        COLOR_CYCLE_FAST,
        RAINBOW_HORIZONTAL_SLOW,
        RAINBOW_HORIZONTAL_FAST,
        RAINBOW_VERTICAL_SLOW,
        COLOR_CYCLE_RAINBOW_VERTICAL_FAST,
    ) = range(7)
