from game.models.entity import WorldEntity
from game.models.point import Point


class UndefinedIo(WorldEntity):
    def __init__(self, relative_entity_id: int, pos: Point) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
