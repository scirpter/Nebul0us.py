from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity


class Wall(WorldEntity):

    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        z: float,
        a0: float,
        b0: float,
        c0: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.z: float = z
        self.a0: float = a0
        self.b0: float = b0
        self.c0: float = c0
