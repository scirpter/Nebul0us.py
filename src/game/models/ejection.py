from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity
from game.models.point import Point


class Ejection(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        pos: Point,
        from_player_entity_id: RELATIVE_ENTITY_ID | None = None,
        mass: float | None = None,
        angle: float | None = None,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.from_player_entity_id: RELATIVE_ENTITY_ID | None = from_player_entity_id
        self.mass: float | None = mass
        self.angle: float | None = angle
