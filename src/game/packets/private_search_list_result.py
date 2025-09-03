from __future__ import annotations
from game.enums.game_mode import GAME_MODE
from game.enums.split_multiplier import SPLIT_MULTIPLIER
from game.enums.world_size import WORLD_SIZE
from game.models.client.private_search_list import SearchListEntry
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models.client.client import Client


class PRIVATE_SEARCH_LIST_RESULT(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        s = ByteArray(self.stream)
        s.read_byte()
        result_ct = s.read_byte()

        entries: list[SearchListEntry] = []

        for _ in range(result_ct):
            _room_id = s.read_int()
            players_in_lobby = s.read_byte()
            max_players = s.read_byte()
            game_mode = GAME_MODE(s.read_byte())
            world_size = WORLD_SIZE(s.read_byte())
            b10 = s.read_byte()
            _z5 = ((b10 & 4) >> 2) == 1
            _z6 = ((b10 & 8) >> 3) == 1
            allow_mass_boost = ((b10 & 16) >> 4) == 1
            split_multiplier = SPLIT_MULTIPLIER((b10 & 96) >> 5)
            _z8 = (b10 & 128) >> 7 == 1
            room_name = s.read_utf()
            b11 = s.read_byte()
            _i9 = b11 & 7
            _z9 = ((b11 & 8) >> 3) == 1
            host_account_id = s.read_int()
            if host_account_id != -1:
                host_name = s.read_utf()
                barrlen = s.read_byte()
                s.read_raw(barrlen)
            else:
                host_name = ""

            entries.append(
                SearchListEntry(
                    room_id=_room_id,
                    name=room_name,
                    game_mode=game_mode,
                    game_size=world_size,
                    max_players=max_players,
                    host_name=host_name,
                    host_account_id=host_account_id,
                    players_in_lobby=players_in_lobby,
                    split_multiplier=split_multiplier,
                    allow_mass_boost=allow_mass_boost,
                )
            )
        self.client.private_search_list.token = s.read_int()
        self.client.private_search_list.entries = entries
