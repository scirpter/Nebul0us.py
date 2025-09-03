from enum import Enum


class SPELL_TYPE(Enum):
    (
        FREEZE,
        POISON,
        BOMB,
        SHOCK,
        SPEED,
        SHIELD,
        RECOMBINE,
        HEAL,
        ATTRACTOR,
        HOOK,
        BLIND,
        RNG,
        TP,
        SWAP,
        PUSH,
        PHASE,
        UNUSED_1,
        UNUSED_2,
        MAGNET,
        SHROOM,
        CLONE,
        RADIATION,
        MINIMAP,
        UNKNOWN,
    ) = range(24)
