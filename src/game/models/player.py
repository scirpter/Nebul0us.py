import math
from game.models.blob import Blob
from game.models.entity import WorldEntity
from game.models.point import Point


class Player(WorldEntity):
    def __init__(self, relative_entity_id: int) -> None:
        super().__init__(relative_entity_id)

        self.name: str = "NULL"
        self.account_id: int = -1
        self.cr2_token2: int | None = None
        self.clan_name: str | None = None
        self.level: int | None = None
        self.skin_id: int | None = None
        self.xp: int | None = None
        self.hat_id: int | None = None
        self.halo_id: int | None = None
        self.blobs: dict[int, Blob] = {}
        self.particles_id: int | None = None
        self.cycle_id: int | None = None
        self.M: int | None = None

    def get_mass(self) -> float:
        return sum(blob.mass for blob in self.blobs.copy().values())

    def is_ingame_bot(self) -> bool:
        return self.account_id == -2

    def is_dead(self) -> bool:
        return len(self.blobs) == 0

    def get_avg_radius(self) -> float:
        return math.sqrt(self.get_mass() / math.pi)

    def get_avg_pos(self) -> Point | None:
        blobs = self.blobs.copy().values()
        if not blobs:
            return None
        blen: int = len(blobs)
        return Point(
            sum(blob.pos.x for blob in blobs) / blen,
            sum(blob.pos.y for blob in blobs) / blen,
        )

    def get_blob_sorted(self, rank: int = 0) -> Blob | None:
        """Gets the blob by rank, sorted by mass. Rank 0 is the largest blob"""
        if len(self.blobs) <= rank:
            return None
        return sorted(
            self.blobs.copy().values(), key=lambda blob: blob.mass, reverse=True
        )[rank]
