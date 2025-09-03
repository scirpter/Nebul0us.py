from game.models.entity import WorldEntity
from game.models.point import Point


class Blob(WorldEntity):
    def __init__(
        self, relative_entity_id: int, pos: Point, mass: float, p: int
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.mass: float = mass
        self.p: int = p

    def update(self, pos: Point, mass: float, p: int) -> None:
        self.pos = pos
        self.mass = mass
        self.p = p
