from helpers.java_data_stream import JavaDataInputStream
from datetime import datetime


def GET_COMMON_REQUEST_STAMP() -> int:
    """unix nano / 1000000"""
    return int(datetime.now().timestamp() * 1000)


def RNATIVE_OBJ_DATA_RELATIVE(
    stream: JavaDataInputStream, f1: float, f2: float
) -> float:
    v0: int = stream.read_byte() & 0xFF
    v1: int = stream.read_byte() & 0xFF
    v2: int = stream.read_byte() & 0xFF

    return ((v0 * 65536.0) + (v1 * 256.0) + v2) * (f2 - f1) / 16777215.0 + f1


def RNATIVE_OBJ_DATA_RELATIVE_2(stream: JavaDataInputStream, f: float) -> float:
    v0: int = stream.read_byte() & 0xFF
    v1: int = stream.read_byte() & 0xFF
    v2: int = stream.read_byte() & 0xFF

    return (((f - 0.0) * ((v0 << 16) + (v1 << 8)) + v2) / 1.6777215e7) + 0.0


def RNATIVE_LE_SHORT_INT(stream: JavaDataInputStream) -> int:
    v0: int = stream.read_byte() & 0xFF
    v1: int = stream.read_byte() & 0xFF
    v2: int = stream.read_byte() & 0xFF

    return (v0 << 16) + (v1 << 8) + v2


def RNATIVE_OBJ_ANGLE(stream: JavaDataInputStream, f1: float, f2: float) -> float:
    v0: int = stream.read_byte() & 0xFF
    return v0 * (f2 - f1) / 255.0 + f1


def RNATIVE_INTERPOLATE(stream: JavaDataInputStream, f1: float, f2: float) -> float:
    short_val: int = stream.read_short() & 65535
    return short_val * (f2 - f1) / 65535.0 + f1


def NATIVE_GET_CONTROL_ANGLE(f1: float, f2: float) -> float:
    return ((f1 - 0.0) * 65535.0) / (f2 - 0.0)


def RNATIVE_APPLY_SCALING_FACTOR(stream: JavaDataInputStream, f: float) -> float:
    v0: int = stream.read_short() & 65535
    return ((f - 0.0) * v0) / 65535.0 + 0.0
