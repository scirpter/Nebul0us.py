import math
from base.custom_types import RELATIVE_ENTITY_ID
from game.enums.hole_type import HOLE_TYPE
from game.enums.item_type import ITEM_TYPE
from game.enums.spell_status import SPELL_STATUS
from game.enums.spell_type import SPELL_TYPE
from game.models.io import UndefinedIo
from game.models.blob import Blob
from game.models.dot import Dot
from game.models.ejection import Ejection
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
from game.sigs import MAP_SIZE_SIG

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


def retarded_func(rb: int) -> int:
    return (rb + 128) % 256


class GAME_UPDATE(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.world_sig: float = 0.0
        self.reliable_mass: int = 0
        self.spectator_count: int = 0
        self.recombine_time: int = 0
        self.player_count: int = 0
        self.event_count: int = 0
        self.io_count: int = 0
        self.ejection_count: int = 0
        self.dot_count: int = 0
        self.hole_count: int = 0
        self.moving_ejection_count: int = 0
        self.item_count: int = 0
        self.jo_count: int = 0
        self.spell_count: int = 0
        self.wall_count: int = 0
        self.r0_count: int = 0
        self.m0_count: int = 0

        self.ios: dict[RELATIVE_ENTITY_ID, UndefinedIo] = {}
        self.ejections: dict[RELATIVE_ENTITY_ID, Ejection] = {}
        self.moving_ejections: dict[RELATIVE_ENTITY_ID, Ejection] = {}
        self.dots: dict[RELATIVE_ENTITY_ID, Dot] = {}
        self.items: dict[RELATIVE_ENTITY_ID, Item] = {}
        self.holes: dict[RELATIVE_ENTITY_ID, Hole] = {}
        self.jos: dict[RELATIVE_ENTITY_ID, UndefinedJo] = {}
        self.players: dict[RELATIVE_ENTITY_ID, Player] = {}
        self.r0s: dict[RELATIVE_ENTITY_ID, UndefinedR0] = {}
        self.spells: dict[RELATIVE_ENTITY_ID, Spell] = {}
        self.walls: dict[RELATIVE_ENTITY_ID, Wall] = {}
        self.m0s: list[UndefinedM0] = []

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        stream.read_byte()  # tick
        stream.read_byte()  # tick
        self.world_sig = RNATIVE_OBJ_DATA_RELATIVE_2(stream, MAP_SIZE_SIG)
        stream.read_byte()
        self.reliable_mass = RNATIVE_LE_SHORT_INT(stream)
        self.spectator_count = retarded_func(stream.read_byte())
        self.recombine_time = retarded_func(stream.read_byte())
        self.player_count = stream.read_byte()
        rb: int = stream.read_byte()
        self.event_count = rb & 31
        self.io_count: int = (rb & 224) >> 5
        self.ejection_count = stream.read_byte()
        self.dot_count = retarded_func(stream.read_byte())
        self.hole_count = stream.read_byte()
        self.moving_ejection_count = stream.read_byte()
        rb2: int = stream.read_byte()
        self.item_count = rb2 & 31
        self.jo_count: int = (rb2 & 224) >> 5
        rb3: int = stream.read_byte()
        self.spell_count = rb3 & 31
        self.wall_count = (rb3 & 224) >> 5
        self.m0_count: int = retarded_func(stream.read_byte())
        self.r0_count: int = stream.read_byte()

        if self.io_count > 0:
            for _ in range(self.io_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.ios[entity_id] = UndefinedIo(entity_id, pos)

        if self.ejection_count > 0:
            for _ in range(self.ejection_count):
                rb4: int = stream.read_byte()
                z8: bool = (rb4 & 1) == 1
                entity_id = RELATIVE_ENTITY_ID((rb4 & 254) >> 1)
                from_player_entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                angle: float = RNATIVE_OBJ_ANGLE(stream, 0, 2 * math.pi)

                if not z8:
                    mass: float = RNATIVE_OBJ_DATA_RELATIVE_2(stream, 500000.0)
                else:  # ejection is deleted
                    mass: float = -math.inf

                self.ejections[entity_id] = Ejection(
                    entity_id, pos, from_player_entity_id, mass, angle
                )

        if self.moving_ejection_count > 0:
            for _ in range(self.moving_ejection_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.moving_ejections[entity_id] = Ejection(entity_id, pos)

        if self.dot_count > 0:
            for _ in range(self.dot_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_short())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.dots[entity_id] = Dot(entity_id, pos)

        if self.item_count > 0:
            for _ in range(self.item_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                type = ITEM_TYPE(stream.read_byte())
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.items[entity_id] = Item(entity_id, pos, type)

        if self.hole_count > 0:
            for _ in range(self.hole_count):
                rb5 = stream.read_byte()
                entity_id = RELATIVE_ENTITY_ID((rb5 & 252) >> 2)
                type = HOLE_TYPE(rb5 & 3)
                y, x = RNATIVE_OBJ_DATA_RELATIVE_2(
                    stream, self.world_sig
                ), RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig)
                pos = Point(x, y)
                mass = RNATIVE_APPLY_SCALING_FACTOR(stream, 62.6)
                self.holes[entity_id] = Hole(entity_id, pos, type, mass)

        if self.jo_count > 0:
            for _ in range(self.jo_count):
                self.jos[RELATIVE_ENTITY_ID(stream.read_byte())] = UndefinedJo(
                    RELATIVE_ENTITY_ID(stream.read_byte()),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_ANGLE(stream, 0, 1),
                )

        if self.player_count > 0:
            for _ in range(self.player_count):
                rb6: int = stream.read_byte()
                entity_id = RELATIVE_ENTITY_ID((rb6 & 254) >> 1)
                player = Player(entity_id)
                z2 = False
                if rb6 & 1 != 0:
                    z2 = True

                m: int = 0
                if z2:
                    m: int = stream.read_byte()
                player.M = m

                blob_count: int = retarded_func(stream.read_byte())

                for _ in range(blob_count):
                    rb7: int = stream.read_byte()
                    z3 = False

                    if rb7 & 1 == 0:
                        z3 = True

                    z4 = False

                    if (rb7 & 128) >> 7 == 1:
                        z4 = True

                    blob_entity_id = RELATIVE_ENTITY_ID((rb7 & 126) >> 1)

                    p: int = 0
                    if z3:
                        p: int = stream.read_short()

                    blob_pos = Point(
                        RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                        RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    )

                    blob_mass: float = -math.inf
                    if not z4:
                        blob_mass = RNATIVE_OBJ_DATA_RELATIVE_2(stream, 500000.0)

                    blob = Blob(blob_entity_id, blob_pos, blob_mass, p)
                    player.blobs.append(blob)

                self.players[player.relative_entity_id] = player

        if self.r0_count > 0:
            for _ in range(self.r0_count):
                rb8: int = stream.read_byte()
                entity_id = RELATIVE_ENTITY_ID(rb8 & 0xF)
                z = False
                if (rb8 & 128) >> 7 != 0:
                    z = True

                h: bool = z
                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                angle: float = RNATIVE_OBJ_ANGLE(stream, 0, math.sqrt(2000))
                self.r0s[entity_id] = UndefinedR0(entity_id, h, pos, angle)

        if self.spell_count > 0:
            for _ in range(self.spell_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                rb9: int = stream.read_byte()
                status = SPELL_STATUS(rb9 & 3)
                type = SPELL_TYPE((rb9 & 252) >> 2)

                if type.value >= SPELL_TYPE.UNKNOWN.value:
                    type = SPELL_TYPE.UNKNOWN

                pos = Point(
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.spells[entity_id] = Spell(entity_id, pos, type, status)

        if self.wall_count > 0:
            for _ in range(self.wall_count):
                entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
                z, a0, b0, c0 = (
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                    RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.world_sig),
                )
                self.walls[entity_id] = Wall(entity_id, z, a0, b0, c0)

        if self.m0_count > 0:
            for _ in range(self.m0_count):
                self.m0s.append(
                    UndefinedM0(
                        retarded_func(stream.read_byte()),
                        retarded_func(stream.read_byte()),
                        stream.read_byte(),
                    )
                )

        if self.event_count > 0:
            for _ in range(self.event_count):
                ...  # TODO: finish this
