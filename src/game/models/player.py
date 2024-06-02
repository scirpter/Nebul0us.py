import math
from base.custom_types import RELATIVE_ENTITY_ID
from game.models.blob import Blob
from game.models.entity import WorldEntity


class Player(WorldEntity):
    def __init__(self, relative_entity_id: RELATIVE_ENTITY_ID) -> None:
        super().__init__(relative_entity_id)

        self.name: str = "NULL"
        self.account_id: int = -1
        self.cr2_token2: int | None
        self.clan_name: str | None
        self.level: int | None
        self.skin_id: int | None
        self.hat_id: int | None
        self.halo_id: int | None
        self.blobs: list[Blob] = []
        self.particles_id: int | None
        self.cycle_id: int | None
        self.M: int | None = None

    def get_mass(self) -> float:
        return sum(blob.mass for blob in self.blobs.copy())

    def is_dead(self) -> bool:
        return len(self.blobs) == 0

    def get_avg_radius(self) -> float:
        return math.sqrt(self.get_mass() / math.pi)

    def get_avg_pos(self) -> tuple[float, float]:
        blobs: list[Blob] = self.blobs.copy()
        return (
            sum(blob.pos.x for blob in blobs) / len(blobs),
            sum(blob.pos.y for blob in blobs) / len(blobs),
        )

    def get_blob_sorted(self, rank: int = 0) -> Blob | None:
        """Gets the blob by rank, sorted by mass. Rank 0 is the largest blob"""
        if len(self.blobs) <= rank:
            return None
        return sorted(self.blobs.copy(), key=lambda blob: blob.mass, reverse=True)[rank]
