from game.models.entity import WorldEntity
from game.models.point import Point


class UndefinedR0(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        h: bool,
        pos: Point,
        angle: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.h: bool = h
        self.pos: Point = pos
        self.angle: float = angle

    def update(self, h: bool, pos: Point, angle: float) -> None:
        self.h = h
        self.pos = pos
        self.angle = angle
