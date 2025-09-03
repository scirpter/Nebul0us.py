from __future__ import annotations
from binascii import hexlify
from random import SystemRandom
from typing import TYPE_CHECKING
from game.enums.packet_type import PACKET_TYPE
from game.packets.connect_result_2 import CONNECT_RESULT_2
from game.packets.game_data import GAME_DATA
from game.packets.game_update import GAME_UPDATE
from game.packets.join_result import JOIN_RESULT
from game.packets.packet import Packet
from game.packets.pong import PONG
from game.packets.private_search_list_result import PRIVATE_SEARCH_LIST_RESULT
from game.packets.session_stats import SESSION_STATS
from game.packets.world_data import WORLD_DATA


if TYPE_CHECKING:
    from game.models.client.client import Client


sysrng = SystemRandom()


def get_packet_class_by_id(i: int) -> type[Packet] | bool:
    try:
        PACKET_TYPE(i)
    except ValueError:
        return False

    match PACKET_TYPE(i):
        case PACKET_TYPE.PONG:
            return PONG
        case PACKET_TYPE.GAME_UPDATE:
            return GAME_UPDATE
        case PACKET_TYPE.CONNECT_RESULT_2:
            return CONNECT_RESULT_2
        case PACKET_TYPE.WORLD_DATA:
            return WORLD_DATA
        case PACKET_TYPE.GAME_DATA:
            return GAME_DATA
        case PACKET_TYPE.SESSION_STATS:
            return SESSION_STATS
        case PACKET_TYPE.JOIN_RESULT:
            return JOIN_RESULT
        case PACKET_TYPE.PRIVATE_SEARCH_LIST_RESULT:
            return PRIVATE_SEARCH_LIST_RESULT
        case _:
            print(
                f"UNHANDLED BUT RECOGNIZED PACKET: {i} 0x{hexlify(i.to_bytes(1, 'big')).decode()}."
            )

    return True


def generate_safe_int32() -> int:
    return sysrng.randint(-2147483648, 2147483647)


def value_equals_any_token(client: Client, value: int) -> bool:
    return value in {
        client.private_search_list.token,
        client.client_data.cr2_token1,
        client.client_data.cr2_token2,
        client.client_data.rng_token1,
        client.client_data.rng_token2,
    }


def ubyte_to_byte(uint_b: int) -> int:
    """convert from unsigned to signed byte"""
    return uint_b - 256 if uint_b > 127 else uint_b
