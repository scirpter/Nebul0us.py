from __future__ import annotations
from game.enums.item_type import ITEM_TYPE
from game.models.dot import Dot
from game.models.ejection import Ejection
from game.models.item import Item
from game.models.player import Player
from game.models.point import Point
from game.natives import RNATIVE_INTERPOLATE, RNATIVE_OBJ_DATA_RELATIVE_2

from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.models.client.client import Client


class GAME_DATA(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        stream.read_byte()
        self.client.client_data.world.id_ = stream.read_int()
        self.client.client_data.world.raw_size = stream.read_float()
        player_count = stream.read_byte()
        ejection_count = stream.read_byte()
        dot_count_offset = stream.read_short()
        dot_count = stream.read_short()
        item_count_offset = stream.read_byte()
        item_count = stream.read_byte()

        for _ in range(player_count):
            player = Player(int(stream.read_byte()))
            stream.read_short()
            stream.read_byte()
            stream.read_int()
            stream.read_int()
            stream.read_byte()
            stream.read_short()
            stream.read_utf()
            player.hat_id = stream.read_byte()
            player.halo_id = stream.read_byte()
            stream.read_byte()
            stream.read_short()
            stream.read_utf()
            stream.read_int()
            stream.read_int()
            player.particles_id = stream.read_byte()
            b_arr1: int = stream.read_byte()
            stream.read_raw(b_arr1)
            player.cycle_id = stream.read_byte()
            stream.read_short()
            RNATIVE_INTERPOLATE(stream, 0.0, 60.0)
            stream.read_int()
            stream.read_int()
            stream.read_byte()
            player.name = stream.read_utf()
            stream.read_byte()
            b_arr2: int = stream.read_byte()
            if b_arr2 > 16:
                raise ValueError("INVALID ALIAS COLORS LENGTH!")

            stream.read_raw(b_arr2)
            player.account_id = stream.read_int()
            player.level = stream.read_short()
            player.clan_name = stream.read_utf()
            b_arr3: int = stream.read_byte()
            stream.read_raw(b_arr3)
            stream.read_byte()
            stream.read_byte()
            self.client.client_data.world.players[player.relative_entity_id] = player

        ejections: dict[int, Ejection] = {}
        for _ in range(ejection_count):
            entity_id = stream.read_byte()
            pos = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
            )
            mass: float = RNATIVE_OBJ_DATA_RELATIVE_2(stream, 500000.0)
            ejections[entity_id] = Ejection(entity_id, pos, None, mass, None)
        self.client.client_data.world.ejections = ejections

        dots: dict[int, Dot] = {}
        for i in range(dot_count):
            entity_id: int = i + dot_count_offset
            pos: Point = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
            )
            dots[entity_id] = Dot(entity_id, pos)
        self.client.client_data.world.dots = dots

        items: dict[int, Item] = {}
        for i in range(item_count):
            entity_id = i + item_count_offset
            type_ = ITEM_TYPE(stream.read_byte())
            pos = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.client.client_data.world.raw_size),
            )
            items[entity_id] = Item(entity_id, pos, type_)
        self.client.client_data.world.items = items
