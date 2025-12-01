from enum import Enum


class HOLE_TYPE(Enum):
    (
        NORMAL,  # gain mass
        SUPERMASSIVE,  # gain a lot of mass
        TELEPORT,  # tp to random other hole in the map with same type
        NEBU,  # if blob size > hole size, blob hitting it will blow up in single peaces
    ) = range(4)
