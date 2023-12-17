from base.custom_types import ENTITY_ID
from game.models.entity import WorldEntity


class Spell(WorldEntity):
    def __init__(
        self,
        relative_entity_id: ENTITY_ID,
        pos: tuple[float, float],
        type_id: int,
        status_id: int,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.type_id: int = type_id
        self.status_id: int = status_id
