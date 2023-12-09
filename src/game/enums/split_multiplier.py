from enum import Enum


class SplitMultiplier(Enum):
    (
        X8,
        X16,
        X32,
        X64,
    ) = range(4)
