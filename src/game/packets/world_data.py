from __future__ import annotations
from typing import TYPE_CHECKING
from game.enums.game_mode import GAME_MODE
from game.enums.world_size import WORLD_SIZE
from game.models.game_leaderboard import LeaderboardEntry
from game.natives import RNATIVE_LE_SHORT_INT
from helpers._io.bytearray import ByteArray
from .packet import Packet

if TYPE_CHECKING:
    from game.models.client.client import Client


def b5_v0_h(v: int) -> int:
    return 2 if (v < 0 or v >= 5) else v


def b5_F_p(b6: int, gamemode_int: int) -> int:
    if gamemode_int != 2:
        if gamemode_int == 3 or gamemode_int == 4:
            return 2 if (b6 == 1 or b6 == 0) else 4
        if gamemode_int not in [6, 8, 32, 37]:
            if gamemode_int == 11 and (b6 in [0, 1, 2]):
                return 3

    return 0


class WORLD_DATA(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        s = ByteArray(self.stream)
        s.read_byte()
        self.client.client_data.world.name = s.read_utf()  # name (k)
        _odd_token = s.read_int()  # f22665m
        _e = s.read_short()  # e
        self.client.client_data.world.game_mode = GAME_MODE(
            s.read_byte()
        )  # f22672t

        b6 = s.read_byte()
        _s_idx = b6 & 3  # f22671s
        if _s_idx < 0 or _s_idx >= 2:
            _s_idx = 1
        _r = b5_v0_h((b6 & 12) >> 2)  # f22670r (variant)

        _n = ((b6 & 16) >> 4) == 1  # f22666n
        _o = ((b6 & 32) >> 5) == 1  # f22667o
        _p = ((b6 & 64) >> 6) == 1  # f22668p
        q = ((b6 & 128) >> 7) == 1  # f22669q

        _f = s.read_byte()  # f22659f
        g = s.read_byte()  # f22660g
        for _ in range(g):
            _j = s.read_short()  # f22662j[i]
            _h_bits = s.read_byte()  # h[i] / f22661i[i] bits
            # if gamemode == battleroyale: ...

        leaderboard_entries: list[LeaderboardEntry] = []
        for _ in range(5):
            _playerid = s.read_byte()  # f22657c[i]
            _playermass = RNATIVE_LE_SHORT_INT(s)

            leaderboard_entries.append(LeaderboardEntry(_playerid, _playermass))

        self.client.client_data.world.leaderboard.update(leaderboard_entries)

        b10 = s.read_byte()
        _u = (b10 & 1) == 1  # f22673u
        _v = (b10 & 0xFE) >> 1  # f22674v

        b11 = s.read_byte()
        w = (b11 & 1) == 1  # f22675w
        self.client.client_data.world.size = WORLD_SIZE(
            (b11 & 126) >> 1
        )  # f22677y index
        _x = ((b11 & 128) >> 7) == 1  # f22676x

        l_len = s.read_byte()  # len(f22664l)
        _l_bytes = s.read_raw(l_len)  # f22664l
        _ = _l_bytes

        if w and not q:
            b12 = s.read_byte()
            _z0 = b12 & 15  # f22678z[0]
            _z1 = (b12 & 240) >> 4  # f22678z[1]

        # Skipping f22649A block (depends on b5.F.p length logic)

        if self.client.client_data.world.game_mode == GAME_MODE.TEAM_DEATHMATCH:
            ip = b5_F_p(_r, self.client.client_data.world.game_mode.value)
            _b13 = s.read_byte()
            if ip > 2:
                _b14 = s.read_byte()
                ...  # skip the rest like wtf

        _b = s.read_byte()  # f22650B
        _c = s.read_byte()  # f22651C
        b15 = s.read_byte()
        _d_map = 0 if (b15 < 0 or b15 >= 5) else b15  # f22652D index
        _e2 = s.read_byte()  # f22653E
        _ = s.read_byte()  # discard one
        _f2 = s.read_int()  # f22654F
        _g2 = s.read_bool()  # f22655G
        self.client.client_data.world.token = s.read_int()  # f22656H
        _r2 = s.read_byte()  # f22670r (final)
