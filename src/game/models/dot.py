from game.models.entity import WorldEntity
from game.models.point import Point


class Dot(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: Point,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos

    def update(self, pos: Point) -> None:
        self.pos = pos
