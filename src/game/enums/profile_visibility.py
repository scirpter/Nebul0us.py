from __future__ import annotations
from enum import Enum


class PROFILE_VISIBILITY(Enum):
    (
        ONLINE,
        APPEAR_OFFLINE,
        HIDDEN,
        DND,
    ) = range(4)

    @staticmethod
    def get_type_from_str(visibility_name: str) -> PROFILE_VISIBILITY:
        return PROFILE_VISIBILITY[visibility_name]

    @staticmethod
    def get_all_string_types() -> list[str]:
        return [visibility.name for visibility in PROFILE_VISIBILITY]
