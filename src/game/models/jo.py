from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity


class UndefinedJo(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        g: float,
        h: float,
        i: float,
        j: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.g: float = g
        self.h: float = h
        self.i: float = i
        self.j: float = j
