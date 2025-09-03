from enum import Enum


class GAME_MODE(Enum):
    (
        FFA,
        FFA_TIME,
        TEAMS,
        TEAMS_TIME,
        CTF,
        SURVIVAL,
        SOCCER,
        FFA_CLASSIC,
        DOMINATION,
        FFA_ULTRA,
        ZOMBIE_APOCALYPSE,  # NOTE: renamed from "ZA"
        PAINT,
        TEAM_DEATHMATCH,
        X,
        X2,
        X3,
        X4,
        X5,
        SPLIT_16X,
        X6,
        X7,
        CAMPAIGN,
        ROYALEDUO,
        X8,
        TRICK_MODE,  # NOTE: renamed from "X9"
        PLASMA_HUNT,  # NOTE: renamed from "X10"
        X11,
        X12,
        X13,
        X14,
        X15,
        X16,
        X17,
        DASH,  # NOTE: renamed from "X18"
        X19,
        CRAZY_SPLIT,
        BATTLE_ROYALE,
        X20,
        X21,
        MEGA_SPLIT,
        CAMPAIGN_2,
        X22,
        RPG,
    ) = range(43)

    @classmethod
    def all(cls) -> list[str]:
        return [mode.name for mode in cls]

    @classmethod
    def from_string(cls, name: str) -> "GAME_MODE":
        for mode in cls:
            if mode.name == name:
                return mode
        raise ValueError(f"Unknown game mode: {name}")
