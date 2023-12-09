from enum import Enum


class ProfileVisibility(Enum):
    (
        ONLINE,
        APPEAR_OFFLINE,
        HIDDEN,
        DND,
    ) = range(4)
