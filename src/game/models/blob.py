from base.custom_types import EntityId
from game.models.entity import WorldEntity


class Blob(WorldEntity):
    def __init__(
        self,
        relative_entity_id: EntityId,
        pos: tuple[float, float],
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.mass: float = mass
