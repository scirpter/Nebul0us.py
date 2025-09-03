from game.models.entity import WorldEntity
from game.models.point import Point


class Ejection(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: Point,
        from_player_entity_id: int | None = None,
        mass: float | None = None,
        angle: float | None = None,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.from_player_entity_id: int | None = from_player_entity_id
        self.mass: float | None = mass
        self.angle: float | None = angle

    def update(
        self,
        pos: Point,
        from_player_entity_id: int | None,
        mass: float | None,
        angle: float | None,
    ) -> None:
        self.pos = pos
        self.from_player_entity_id = from_player_entity_id
        self.mass = mass
        self.angle = angle
