from enum import Enum


class REGION(Enum):
    US_EAST = "US_EAST"
    US_WEST = "US_WEST"
    EU = "EU"
    EAST_ASIA = "EAST_ASIA"
    SOUTH_ASIA = "SOUTH_ASIA"
    SOUTH_AMERICA = "SOUTH_AMERICA"
    AUSTRALIA = "AUSTRALIA"
    JAPAN = "JAPAN"
    MIDDLE_EAST = "MIDDLE_EAST"
    SOUTH_AFRICA = "SOUTH_AFRICA"
    INDIA = "INDIA"
    DEBUG = "DEBUG"
    DEBUG_GLOBAL = "DEBUG_GLOBAL"

    @staticmethod
    def all() -> list[str]:
        return [region.name for region in REGION]
