from base.custom_types import RELATIVE_ENTITY_ID
from game.models.dot import Dot
from game.models.ejection import Ejection
from game.models.item import Item
from game.models.player import Player
from game import enums
from game.models.point import Point
from game.natives import RNATIVE_INTERPOLATE, RNATIVE_OBJ_DATA_RELATIVE_2

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class GAME_DATA(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.world_token: int = 0
        self.raw_world_size: float = 0.0

        self.player_count: int = 0
        self.ejection_count: int = 0
        self.dot_count_offset: int = 0
        self.dot_count: int = 0
        self.item_count_offset: int = 0
        self.item_count: int = 0

        self.players: dict[RELATIVE_ENTITY_ID, Player] = {}
        self.ejections: dict[RELATIVE_ENTITY_ID, Ejection] = {}
        self.dots: dict[RELATIVE_ENTITY_ID, Dot] = {}
        self.items: dict[RELATIVE_ENTITY_ID, Item] = {}

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.world_token = stream.read_int()
        self.raw_world_size = stream.read_float()
        self.player_count = stream.read_byte()
        self.ejection_count = stream.read_byte()
        self.dot_count_offset = stream.read_short()
        self.dot_count = stream.read_short()
        self.item_count_offset = stream.read_byte()
        self.item_count = stream.read_byte()

        for _ in range(self.player_count):
            player = Player(RELATIVE_ENTITY_ID(stream.read_byte()))
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
            stream.read_fully(b_arr1)
            player.cycle_id = stream.read_byte()
            stream.read_short()
            RNATIVE_INTERPOLATE(stream, 0.0, 60.0)
            stream.read_int()
            stream.read_int()
            stream.read_byte()
            player.name = stream.read_utf()
            stream.read_byte()
            b_arr2: int = stream.read_byte()
            if b_arr2 <= 16:
                stream.read_fully(b_arr2)
                player.account_id = stream.read_int()
                player.level = stream.read_short()
                player.clan_name = stream.read_utf()
                b_arr3: int = stream.read_byte()
                stream.read_fully(b_arr3)
                stream.read_byte()
                stream.read_byte()
            else:
                raise ValueError("INVALID ALIAS COLORS LENGTH!")

            self.players[player.relative_entity_id] = player

        for _ in range(self.ejection_count):
            entity_id = RELATIVE_ENTITY_ID(stream.read_byte())
            pos = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
            )
            mass: float = RNATIVE_OBJ_DATA_RELATIVE_2(stream, 500000.0)
            self.ejections[entity_id] = Ejection(entity_id, pos, None, mass, None)

        for i in range(self.dot_count):
            entity_id = RELATIVE_ENTITY_ID(i + self.dot_count_offset)
            pos: Point = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
            )
            self.dots[entity_id] = Dot(entity_id, pos)

        for i in range(self.item_count):
            entity_id = RELATIVE_ENTITY_ID(i + self.item_count_offset)
            type = enums.ITEM_TYPE(stream.read_byte())
            pos = Point(
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
                RNATIVE_OBJ_DATA_RELATIVE_2(stream, self.raw_world_size),
            )
            self.items[entity_id] = Item(entity_id, pos, type)
