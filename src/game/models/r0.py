from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity
from game.models.point import Point


class UndefinedR0(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        h: bool,
        pos: Point,
        angle: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.H: bool = h
        self.pos: Point = pos
        self.angle: float = angle
