from helpers.java_data_stream import JavaDataInputStream
from game.models.client.client import Client
from .packet import Packet


class CONNECT_RESULT_2(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.rng_token1: int = 0
        self.cr2_token1: int = 0
        self.cr2_token2: int = 0
        self.world_token: int = 0

    def parse(self) -> None:
        stream = JavaDataInputStream(self.stream)
        stream.read_byte()
        self.rng_token1 = stream.read_int()
        stream.read_byte()
        self.cr2_token1 = stream.read_int()
        self.cr2_token2 = stream.read_int()
        self.world_token = stream.read_int()
        stream.read_int()
        stream.read_float()
        stream.read_byte()
