from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity
from game.models.point import Point


class Blob(WorldEntity):
    def __init__(
        self, relative_entity_id: RELATIVE_ENTITY_ID, pos: Point, mass: float, p: int
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.mass: float = mass
        self.P: int = p
