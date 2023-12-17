from base.custom_types import ENTITY_ID
from game.models.entity import WorldEntity


class Hole(WorldEntity):
    def __init__(
        self,
        relative_entity_id: ENTITY_ID,
        pos: tuple[float, float],
        type_id: int,
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.type_id: int = type_id
        self.mass: float = mass
