from game import enums
from game.natives import RNATIVE_LE_SHORT_INT

from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class ENTER_GAME_RESULT(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.result: enums.JOIN_RESULT = enums.JOIN_RESULT.UNKNOWN_ERROR
        self.room_name: str = ""
        self.game_mode: enums.GAME_MODE = enums.GAME_MODE.INVALID
        self.room_size: enums.WORLD_SIZE = enums.WORLD_SIZE.NORMAL
        self.split_multiplier: enums.SPLIT_MULTIPLIER = enums.SPLIT_MULTIPLIER.X8

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()

        result: int = stream.read_byte()
        if result >= len(enums.JOIN_RESULT):
            self.result = enums.JOIN_RESULT.UNKNOWN_ERROR
        else:
            self.result = enums.JOIN_RESULT(result)

        if self.result == enums.JOIN_RESULT.SUCCESS:
            read_byte2: int = stream.read_byte()
            e: int = read_byte2
            if e >= 2:
                e = 1

            g = stream.read_byte()
            if g >= 4:
                g = 2

            self.game_mode = enums.GAME_MODE(stream.read_byte())
            stream.read_int()
            stream.read_int()
            stream.read_int()
            self.room_name = stream.read_utf()
            stream.read_byte()
            stream.read_bool()
            stream.read_long()
            stream.read_byte()
            stream.read_int()
            stream.read_bool()
            stream.read_bool()
            stream.read_bool()
            stream.read_int()
            stream.read_bool()
            stream.read_byte()
            stream.read_bool()

            room_size: int = stream.read_byte()
            if room_size >= len(enums.WORLD_SIZE):
                self.room_size = enums.WORLD_SIZE.NORMAL
            else:
                self.room_size = enums.WORLD_SIZE(room_size)

            b_arr: int = stream.read_byte()
            stream.read_fully(b_arr)
            stream.read_bool()

        stream.read_long()

        if self.result == enums.JOIN_RESULT.SUCCESS:
            self.split_multiplier = enums.SPLIT_MULTIPLIER(stream.read_byte())
            stream.read_byte()
            RNATIVE_LE_SHORT_INT(stream)
            stream.read_byte()
            stream.read_int()
            stream.read_bool()
