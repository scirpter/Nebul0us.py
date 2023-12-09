import math
from models.blob import Blob
from models.entity import WorldEntity


class Player(WorldEntity):
    cr2_token_2: int | None
    clan_name: str | None
    level: int | None
    skin_id: int | None
    hat_id: int | None
    halo_id: int | None
    blobs: list[Blob] = []
    particles_id: int | None

    def __init__(self, relative_entity_id: int, name: str, account_id: int) -> None:
        super().__init__(relative_entity_id)
        self.name: str = name
        self.account_id: int = account_id

    def get_mass(self) -> float:
        return sum(blob.mass for blob in self.blobs.copy())

    def is_dead(self) -> bool:
        return len(self.blobs) == 0

    def get_avg_radius(self) -> float:
        return math.sqrt(self.get_mass() / math.pi)

    def get_avg_pos(self) -> tuple[float, float]:
        blobs: list[Blob] = self.blobs.copy()
        return (
            sum(blob.pos[0] for blob in blobs) / len(blobs),
            sum(blob.pos[1] for blob in blobs) / len(blobs),
        )

    def get_blob_sorted(self, rank: int = 0) -> Blob | None:
        """Gets the blob by rank, sorted by mass. Rank 0 is the largest blob"""
        if len(self.blobs) <= rank:
            return None
        return sorted(self.blobs.copy(), key=lambda blob: blob.mass, reverse=True)[rank]
