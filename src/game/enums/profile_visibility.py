from enum import Enum


class PROFILE_VISIBILITY(Enum):
    (
        ONLINE,
        APPEAR_OFFLINE,
        HIDDEN,
        DND,
    ) = range(4)
