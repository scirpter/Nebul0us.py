from base.custom_types import RELATIVE_ENTITY_ID
from game.enums.hole_type import HOLE_TYPE
from game.models.entity import WorldEntity
from game.models.point import Point


class Hole(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        pos: Point,
        type: HOLE_TYPE,
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.type: HOLE_TYPE = type
        self.mass: float = mass
