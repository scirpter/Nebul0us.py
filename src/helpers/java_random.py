# type: ignore
import time
import math


class JavaRandom:
    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            seed = int(time.time() * 1000)
        self.seed = seed
        self.next_next_gaussian = None

    def set_seed(self, seed: int) -> None:
        self.seed = seed

    @property
    def seed(self) -> int:
        return self._seed  # type: ignore

    @seed.setter
    def seed(self, seed: int) -> None:
        self._seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits: int) -> int:
        if bits < 1:
            bits = 1
        elif bits > 32:
            bits = 32

        self._seed = (self._seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        retval = self._seed >> (48 - bits)

        # Python and Java don't really agree on how ints work. This converts
        # the unsigned generated int into a signed int if necessary.
        if retval & (1 << 31):
            retval -= 1 << 32

        return retval

    def next_bytes(self, l: list[int]) -> None:  # noqa
        """
        Replace every item in `l` with a random byte.
        """

        for i in range(0, len(l)):
            if not i % 4:
                n = self.next_int()
            b = n & 0xFF
            # Flip signs. Ugh.
            if b & 0x80:
                b -= 0x100
            l[i] = b
            n >>= 8

    def next_int(self, n: int | None = None) -> int:
        if n is None:
            return self.next(32)

        if n <= 0:
            raise ValueError("Argument must be positive!")

        if not (n & (n - 1)):
            return (n * self.next(31)) >> 31

        bits = self.next(31)
        val = bits % n
        while (bits - val + n - 1) < 0:
            bits = self.next(31)
            val = bits % n

        return val

    def next_long(self) -> int:
        return (self.next(32) << 32) + self.next(32)

    def next_boolean(self) -> bool:
        return bool(self.next(1))

    def next_float(self) -> float:
        return self.next(24) / float(1 << 24)

    def next_double(self) -> float:
        return ((self.next(26) << 27) + self.next(27)) / float(1 << 53)

    def next_gaussian(self) -> float:
        if self.next_next_gaussian is None:
            s = 0
            v1 = 0
            v2 = 0
            while s == 0 or s >= 1:
                v1: float = 2 * self.next_double() - 1
                v2: float = 2 * self.next_double() - 1
                s: float = v1 * v1 + v2 * v2
            multiplier: float = math.sqrt(-2 * math.log(s) / s)
            self.next_next_gaussian: float = v2 * multiplier
            return v1 * multiplier
        else:
            retval: float = self.next_next_gaussian
            self.next_next_gaussian = None
            return retval
