from __future__ import annotations
from enum import Enum


class PACKET_TYPE(Enum):
    KEEP_ALIVE = 0x7F
    CONTROL = 0x02
    CONNECT_REQUEST_3 = 0x7D
    PING = 0x85
    PONG = 0x86
    DISCONNECT = 0x07
    GAME_UPDATE = 0x16
    CONNECT_RESULT_2 = 0x01
    BASIC_PING = 0x75

    GAME_CHAT_MESSAGE = 0x89
    WORLD_DATA = 0x14
    GAME_DATA = 0x4B

    JOIN_REQUEST = 0x0A  # we start playing
    JOIN_RESULT = 0x0B  # other player starts playing

    SESSION_STATS = 0x69

    SPECTATE_GAME_REQUEST = 0x38
    ENTER_GAME_REQUEST = 0x28

    PRIVATE_SEARCH_LIST_RESULT = 0x18
    PRIVATE_SEARCH_LIST_REQUEST = 0x17

    CREATE_SKILL_TREE_UPGRADE = 0x8D

    @staticmethod
    def get_type_from_str(packet_name: str) -> PACKET_TYPE | None:
        if packet_name not in PACKET_TYPE.__members__:
            return None
        return PACKET_TYPE[packet_name]
