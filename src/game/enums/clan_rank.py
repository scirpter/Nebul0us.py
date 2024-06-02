from enum import Enum


class CLAN_RANK(Enum):
    (
        INVALID,
        MEMBER,
        ADMIN,
        LEADER,
        ELDER,
        DIAMOND,
        INITIATE,
    ) = range(7)
