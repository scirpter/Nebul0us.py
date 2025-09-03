from __future__ import annotations
import math
from game.enums.hole_type import HOLE_TYPE
from game.enums.item_type import ITEM_TYPE
from game.enums.spell_status import SPELL_STATUS
from game.enums.spell_type import SPELL_TYPE
from game.models.io import UndefinedIo
from game.models.blob import Blob
from game.models.hole import Hole
from game.models.item import Item
from game.models.jo import UndefinedJo
from game.models.m0 import UndefinedM0
from game.models.player import Player
from game.models.point import Point
from game.models.r0 import UndefinedR0
from game.models.spell import Spell
from game.models.wall import Wall
from game.natives import (
    RNATIVE_APPLY_SCALING_FACTOR,
    RNATIVE_LE_SHORT_INT,
    RNATIVE_OBJ_ANGLE,
    RNATIVE_OBJ_DATA_RELATIVE_2,
)
from helpers._io.bytearray import ByteArray
from .packet import Packet


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.models.client.client import Client


def switch_sign(rb: int) -> int:
    return (rb + 128) % 256


class GAME_UPDATE(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)

        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        stream.read_byte()

        self.client.client_data.world.control_tick = stream.read_byte()
        self.client.client_data.world.tick = stream.read_byte()
        if not self.client.client_data.world.raw_size:
            return

        world_sig = RNATIVE_OBJ_DATA_RELATIVE_2(
            stream, self.client.client_data.world.raw_size
        )
        stream.read_byte()
        self.client.player_data.fast_local_mass = RNATIVE_LE_SHORT_INT(stream)
        self.client.client_data.world.spectator_count = switch_sign(
            stream.read_byte()
        )
        self.client.player_data.recombine_time = switch_sign(stream.read_byte())
        player_count = stream.read_byte()
        rb: int = stream.read_byte()
        event_count = rb & 31
        io_count: int = (rb & 224) >> 5
        ejection_count = stream.read_byte()
        dot_count = switch_sign(stream.read_byte())
        hole_count = stream.read_byte()
        moving_ejection_count = stream.read_byte()
        rb2: int = stream.read_byte()
        item_count = rb2 & 31
        jo_count: int = (rb2 & 224) >> 5
        rb3: int = stream.read_byte()
        spell_count = rb3 & 31
        wall_count = (rb3 & 224) >> 5
        m0_count: int = switch_sign(stream.read_byte())
        r0_count: int = stream.read_byte()

        if io_count > 0:
            for _ in range(io_count):
                entity_id = stream.read_byte()
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                self.client.client_data.world.ios[entity_id] = UndefinedIo(
                    entity_id, pos
                )

        if ejection_count > 0:
            for _ in range(ejection_count):
                rb4: int = stream.read_byte()
                z8: bool = (rb4 & 1) == 1
                entity_id = (rb4 & 254) >> 1

                _from_player_entity_id = stream.read_byte()
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                angle: float = RNATIVE_OBJ_ANGLE(stream, 0, 2 * math.pi)

                if not z8:
                    mass: float = RNATIVE_OBJ_DATA_RELATIVE_2(stream, 500000.0)
                else:  # ejection is deleted
                    mass: float = -math.inf

        if moving_ejection_count > 0:
            for _ in range(moving_ejection_count):
                entity_id: int = stream.read_byte()
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )

        if dot_count > 0:
            for _ in range(dot_count):
                entity_id = stream.read_short()
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )

        if item_count > 0:
            items: dict[int, Item] = {}
            for _ in range(item_count):
                entity_id = stream.read_byte()
                type_ = ITEM_TYPE(stream.read_byte())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
            self.client.client_data.world.items = items

        if hole_count > 0:
            holes: dict[int, Hole] = {}
            for _ in range(hole_count):
                rb5 = stream.read_byte()
                entity_id = (rb5 & 252) >> 2
                type_ = HOLE_TYPE(rb5 & 3)
                y, x = (
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                pos = Point(x, y)
                mass = RNATIVE_APPLY_SCALING_FACTOR(stream, 62.6)
                if mass == 0:
                    continue
                holes[entity_id] = Hole(entity_id, pos, type_, mass)
            self.client.client_data.world.holes = holes

        if jo_count > 0:
            for _ in range(jo_count):
                entity_id = stream.read_byte()
                jog, joh, joi, joj = (
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_ANGLE(stream, 0.0, 1.0),
                )
                self.client.client_data.world.jos[entity_id] = UndefinedJo(
                    entity_id, jog, joh, joi, joj
                )

        if player_count > 0:
            for _ in range(player_count):
                b12: int = stream.read_byte()
                entity_id = (b12 & 254) >> 1
                player: Player | None = (
                    self.client.client_data.world.players.get(entity_id)
                )
                if not player:
                    player = Player(entity_id)
                    self.client.client_data.world.players[entity_id] = player

                if (b12 & 1) != 0:
                    player.M = stream.read_byte()
                else:
                    player.M = 0

                blob_count: int = switch_sign(stream.read_byte())
                blobs: dict[int, Blob] = {}
                for _ in range(blob_count):
                    b13: int = stream.read_byte()
                    z6: bool = (b13 & 1) == 1
                    z7 = ((b13 & 128) >> 7) == 1
                    blob_id = (b13 & 126) >> 1

                    if z6:
                        p = stream.read_short()
                    else:
                        p = 0

                    blob_pos = Point(
                        RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                        RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    )

                    if z7:
                        blob_mass = -math.inf
                    else:
                        blob_mass = RNATIVE_OBJ_DATA_RELATIVE_2(
                            stream, 500000.0
                        )

                    blobs[blob_id] = Blob(blob_id, blob_pos, blob_mass, p)
                player.blobs = blobs

        if r0_count > 0:
            for _ in range(r0_count):
                rb8: int = stream.read_byte()
                entity_id = rb8 & 0xF
                z = False
                if (rb8 & 128) >> 7 != 0:
                    z = True

                h: bool = z
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                angle: float = RNATIVE_OBJ_ANGLE(stream, 0, math.sqrt(2000))
                self.client.client_data.world.r0s[entity_id] = UndefinedR0(
                    entity_id, h, pos, angle
                )

        if spell_count > 0:
            for _ in range(spell_count):
                entity_id = stream.read_byte()
                rb9: int = stream.read_byte()
                status = SPELL_STATUS(rb9 & 3)
                type_ = SPELL_TYPE((rb9 & 252) >> 2)

                if type_.value >= SPELL_TYPE.UNKNOWN.value:
                    type_ = SPELL_TYPE.UNKNOWN

                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                self.client.client_data.world.spells[entity_id] = Spell(
                    entity_id, pos, type_, status
                )

        if wall_count > 0:
            for _ in range(wall_count):
                entity_id = stream.read_byte()
                z, a0, b0, c0 = (
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, world_sig),
                )
                self.client.client_data.world.walls[entity_id] = Wall(
                    entity_id, z, a0, b0, c0
                )

        if m0_count > 0:
            for _ in range(m0_count):
                entity_id, e0, f0 = (
                    switch_sign(stream.read_byte()),
                    switch_sign(stream.read_byte()),
                    stream.read_byte(),
                )
                self.client.client_data.world.m0s[entity_id] = UndefinedM0(
                    entity_id, e0, f0
                )

        if event_count > 0:
            for _ in range(event_count):
                ...  # TODO: finish this
