from base.custom_types import EntityId
from game.models.entity import WorldEntity


class Dot(WorldEntity):
    def __init__(
        self,
        relative_entity_id: EntityId,
        pos: tuple[float, float],
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
