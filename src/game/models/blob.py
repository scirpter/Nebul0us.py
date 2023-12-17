from base.custom_types import ENTITY_ID
from game.models.entity import WorldEntity


class Blob(WorldEntity):
    def __init__(
        self,
        relative_entity_id: ENTITY_ID,
        pos: tuple[float, float],
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.mass: float = mass
