from __future__ import annotations

import io
import struct
from typing import Self


class ByteArray:
    def __init__(self, stream: bytes | None = None) -> None:
        self._stream: io.BytesIO = (
            io.BytesIO(stream) if stream is not None else io.BytesIO()
        )
        self.bytes_written: int = 0

    def data(self) -> bytes:
        return self._stream.getvalue()

    def space_left(self) -> int:
        return self._stream.getbuffer().nbytes - self.bytes_written

    def _read_exact(self, n: int) -> bytes:
        if n < 0:
            raise ValueError("n must be non-negative")
        buf = bytearray()
        while len(buf) < n:
            chunk = self._stream.read(n - len(buf))
            if not chunk:
                raise EOFError("Unexpected end of stream")
            buf.extend(chunk)
        return bytes(buf)

    def write_raw(self, b: bytes) -> Self:
        written: int = self._stream.write(b)
        # if written is None:
        #     # Some streams return None but did write all bytes (rare). Assume full write.
        #     written = len(b)
        if written != len(b):
            raise io.BlockingIOError("Failed to write all bytes")
        self.bytes_written += written
        return self

    def flush(self) -> None:
        if hasattr(self._stream, "flush"):
            self._stream.flush()

    def read_bool(self) -> bool:
        return self.read_unsigned_byte() != 0

    def read_byte(self) -> int:
        # signed 8-bit (-128..127)
        return struct.unpack(">b", self._read_exact(1))[0]

    def read_unsigned_byte(self) -> int:
        return struct.unpack(">B", self._read_exact(1))[0]

    def read_short(self) -> int:
        # signed 16-bit (-32768..32767)
        return struct.unpack(">h", self._read_exact(2))[0]

    def read_unsigned_short(self) -> int:
        return struct.unpack(">H", self._read_exact(2))[0]

    def read_char(self) -> str:
        # Java char is 16-bit code unit; return a 1-character Python string
        code_unit = self.read_unsigned_short()
        return chr(code_unit)

    def read_int(self) -> int:
        # signed 32-bit
        return struct.unpack(">i", self._read_exact(4))[0]

    def read_long(self) -> int:
        # signed 64-bit
        return struct.unpack(">q", self._read_exact(8))[0]

    def read_float(self) -> float:
        return struct.unpack(">f", self._read_exact(4))[0]

    def read_double(self) -> float:
        return struct.unpack(">d", self._read_exact(8))[0]

    def read_raw(self, n: int) -> bytes:
        return self._read_exact(n)

    def read_fully_into(
        self, buf: bytearray, off: int = 0, length: int | None = None
    ) -> None:
        """
        Java-like readFully into a provided buffer, raising EOFError if insufficient bytes.
        """
        if length is None:
            length = len(buf) - off
        if off < 0 or length < 0 or off + length > len(buf):
            raise ValueError("Invalid offset/length for target buffer")
        data = self._read_exact(length)
        buf[off : off + length] = data

    def skip_bytes(self, n: int) -> int:
        """
        Attempts to skip n bytes by reading and discarding.
        Returns the actual number of bytes skipped (like Java).
        """
        if n <= 0:
            return 0
        remaining = n
        chunk_size = 8192
        skipped = 0
        while remaining > 0:
            to_read = min(remaining, chunk_size)
            chunk = self._stream.read(to_read)
            if not chunk:
                break
            read_len = len(chunk)
            skipped += read_len
            remaining -= read_len
        return skipped

    def read_utf(self) -> str:
        """
        Reads a string encoded in Java's modified UTF-8 with a 2-byte unsigned length prefix.
        """
        utflen = self.read_unsigned_short()
        data = self._read_exact(utflen)
        return self._decode_modified_utf8(data)

    # ----------------------------
    # Write methods (DataOutput)
    # ----------------------------
    def write_bool(self, v: bool) -> Self:
        self.write_raw(b"\x01" if v else b"\x00")
        return self

    def write_byte(self, v: int) -> Self:
        self.write_raw(bytes([v & 0xFF]))
        return self

    def write_short(self, v: int) -> Self:
        # Write low 16 bits big-endian (matches Java behavior)
        self.write_raw(bytes([(v >> 8) & 0xFF, v & 0xFF]))
        return self

    def write_char(self, v: str | int) -> Self:
        # Accept a single-character string or a 0..0xFFFF int code unit
        if isinstance(v, str):
            if len(v) != 1:
                raise ValueError("writeChar expects a single character string")
            code_unit = ord(v)
        else:
            code_unit = int(v)
        if not (0 <= code_unit <= 0xFFFF):
            raise ValueError("char code unit must be in range 0..0xFFFF")
        self.write_raw(bytes([(code_unit >> 8) & 0xFF, code_unit & 0xFF]))
        return self

    def write_int(self, v: int) -> Self:
        self.write_raw(struct.pack(">I", v & 0xFFFFFFFF))
        return self

    def write_long(self, v: int) -> Self:
        self.write_raw(struct.pack(">Q", v & 0xFFFFFFFFFFFFFFFF))
        return self

    def write_float(self, v: float) -> Self:
        self.write_raw(struct.pack(">f", float(v)))
        return self

    def write_double(self, v: float) -> Self:
        self.write_raw(struct.pack(">d", float(v)))
        return self

    def write_bytes(self, s: bytes | bytearray | memoryview) -> Self:
        # Raw bytes (like Java's write(byte[]))
        self.write_raw(bytes(s))
        return self

    def write_utf(self, s: str) -> Self:
        """
        Writes a string in Java's modified UTF-8 with a 2-byte unsigned length prefix.
        Max encoded length is 65535 bytes.
        """
        data = self._encode_modified_utf8(s)
        if len(data) > 0xFFFF:
            raise ValueError("Encoded UTF string too long (exceeds 65535 bytes)")
        self.write_raw(struct.pack(">H", len(data)))
        self.write_raw(data)
        return self

    # ----------------------------
    # Modified UTF-8 (Java-compatible) helpers
    # ----------------------------
    @staticmethod
    def _encode_modified_utf8(s: str) -> bytes:
        """
        Encode Python str to Java's modified UTF-8:
        - U+0000 encoded as 0xC0 0x80 (no 0x00 bytes appear).
        - U+0001..U+007F as single byte.
        - U+0080..U+07FF as two bytes.
        - U+0800..U+FFFF as three bytes.
        - Supplementary characters (> U+FFFF) are first converted to UTF-16 surrogate pairs,
          then each 16-bit code unit is encoded per the above rules (matching Java behavior).
        """
        # Convert to UTF-16 code units (big-endian, no BOM)
        utf16_be = s.encode("utf-16-be")
        out = bytearray()
        for i in range(0, len(utf16_be), 2):
            cu = (utf16_be[i] << 8) | utf16_be[i + 1]  # 16-bit code unit
            if cu == 0x0000:
                out.extend(b"\xc0\x80")
            elif cu <= 0x007F:
                out.append(cu & 0x7F)
            elif cu <= 0x07FF:
                out.append(0xC0 | ((cu >> 6) & 0x1F))
                out.append(0x80 | (cu & 0x3F))
            else:
                out.append(0xE0 | ((cu >> 12) & 0x0F))
                out.append(0x80 | ((cu >> 6) & 0x3F))
                out.append(0x80 | (cu & 0x3F))
        return bytes(out)

    @staticmethod
    def _decode_modified_utf8(data: bytes) -> str:
        """
        Decode bytes encoded with Java's modified UTF-8 into Python str.
        This reconstructs UTF-16 code units and then decodes as UTF-16 BE.
        """
        i = 0
        units = bytearray()
        n = len(data)
        while i < n:
            b0 = data[i]
            i += 1
            if (b0 & 0x80) == 0:
                # Single-byte: 0xxxxxxx
                cu = b0 & 0x7F
                # In strict modified UTF-8, 0x00 should not appear as a single byte.
                # However, to be permissive, accept it.
                units.append((cu >> 8) & 0xFF)
                units.append(cu & 0xFF)
            elif (b0 & 0xE0) == 0xC0:
                # Two-byte: 110xxxxx 10xxxxxx
                if i >= n:
                    raise UnicodeDecodeError(
                        "mutf8", data, i - 1, i, "unexpected end in 2-byte sequence"
                    )
                b1 = data[i]
                i += 1
                if (b1 & 0xC0) != 0x80:
                    raise UnicodeDecodeError(
                        "mutf8", data, i - 1, i, "invalid continuation byte"
                    )
                cu = ((b0 & 0x1F) << 6) | (b1 & 0x3F)
                units.append((cu >> 8) & 0xFF)
                units.append(cu & 0xFF)
            elif (b0 & 0xF0) == 0xE0:
                # Three-byte: 1110xxxx 10xxxxxx 10xxxxxx
                if i + 1 >= n:
                    raise UnicodeDecodeError(
                        "mutf8", data, i - 1, i, "unexpected end in 3-byte sequence"
                    )
                b1 = data[i]
                b2 = data[i + 1]
                i += 2
                if (b1 & 0xC0) != 0x80 or (b2 & 0xC0) != 0x80:
                    raise UnicodeDecodeError(
                        "mutf8", data, i - 2, i, "invalid continuation bytes"
                    )
                cu = ((b0 & 0x0F) << 12) | ((b1 & 0x3F) << 6) | (b2 & 0x3F)
                units.append((cu >> 8) & 0xFF)
                units.append(cu & 0xFF)
            else:
                # Modified UTF-8 never uses 4-byte sequences
                raise UnicodeDecodeError(
                    "mutf8", data, i - 1, i, "invalid leading byte for modified UTF-8"
                )
        return units.decode("utf-16-be")
