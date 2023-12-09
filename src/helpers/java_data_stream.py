from __future__ import annotations
import io
import struct


class JavaDataInputStream:
    def __init__(self, data: bytes = b"") -> None:
        self.stream = io.BytesIO(data)

    def get_data(self) -> bytes:
        return self.stream.getvalue()

    def space_left(self) -> int:
        return len(self.get_data()) - self.stream.tell()

    def skip(self, amount: int) -> None:
        self.stream.seek(amount, io.SEEK_CUR)

    def to_hex_string(self) -> str:
        return " ".join(f"{byte:02X}" for byte in self.get_data())

    def read_byte(self) -> int:
        return int.from_bytes(self.stream.read(1), "big", signed=True)

    def read_bool(self) -> bool:
        return bool(self.read_byte())

    def read_short(self) -> int:
        return int.from_bytes(self.stream.read(2), "big", signed=True)

    def read_int(self) -> int:
        return int.from_bytes(self.stream.read(4), "big", signed=True)

    def read_long(self) -> int:
        return int.from_bytes(self.stream.read(8), "big", signed=True)

    def read_float(self) -> float:
        return struct.unpack(">f", self.stream.read(4))[0]

    def read_double(self) -> float:
        return struct.unpack(">d", self.stream.read(8))[0]

    def read_fully(self, length: int) -> bytes:
        return self.stream.read(length)

    def read_utf(self) -> str:
        length: int = self.read_short()
        return self.stream.read(length).decode("utf-8")


class JavaDataOutputStream:
    def __init__(self) -> None:
        self.stream = io.BytesIO()

    def get_data(self) -> bytes:
        return self.stream.getvalue()

    def write_byte(self, value: int) -> JavaDataOutputStream:
        self.stream.write(value.to_bytes(1, "big", signed=True))
        return self

    def write_bool(self, value: bool) -> JavaDataOutputStream:
        self.write_byte(int(value))
        return self

    def write_short(self, value: int) -> JavaDataOutputStream:
        self.stream.write(value.to_bytes(2, "big", signed=True))
        return self

    def write_int(self, value: int) -> JavaDataOutputStream:
        self.stream.write(value.to_bytes(4, "big", signed=True))
        return self

    def write_long(self, value: int) -> JavaDataOutputStream:
        self.stream.write(value.to_bytes(8, "big", signed=True))
        return self

    def write_float(self, value: float) -> JavaDataOutputStream:
        self.stream.write(struct.pack(">f", value))
        return self

    def write_double(self, value: float) -> JavaDataOutputStream:
        self.stream.write(struct.pack(">d", value))
        return self

    def write_fully(self, data: bytes) -> JavaDataOutputStream:
        self.stream.write(data)
        return self

    def write_utf(self, value: str) -> JavaDataOutputStream:
        data: bytes = value.encode("utf-8")
        self.write_short(len(data))
        self.stream.write(data)
        return self
