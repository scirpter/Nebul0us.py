from enum import Enum


class RPG_SKILLTREE_UPGRADE(Enum):
    (
        NONE,
        SPEED_PERM_1,
        SPEED_DOT_BOOST,
        SPEED_SO_BOOST,
        SPEED_BLOB_BOOST,
        SPEED_PERM_2,
        EJECT_SPEED_1,
        EJECT_MASS_PRESERVATION,
        EJECT_MASS,
        EJECT_DISTANCE,
        EJECT_SPEED_2,
        SPLIT_SPEED_1,
        SPLIT_BIAS,
        SPLIT_DISTANCE,
        SPLIT_ALLOWANCE,
        SPLIT_SPEED_2,
        RECOMBINE_DURATION_1,
        RECOMBINE_DOT_BOOST,
        RECOMBINE_SO_BOOST,
        RECOMBINE_BLOB_BOOST,
        RECOMBINE_DURATION_2,
        POWER_HUNGRY,
        FARMER,
        INDESTRUCTIBLE,
        EJECTOR,
    ) = range(25)
