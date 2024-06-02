from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity
from game.models.point import Point


class Dot(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        pos: Point,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
