from base.custom_types import ENTITY_ID
from game.models.entity import WorldEntity


class Ejection(WorldEntity):
    def __init__(
        self,
        relative_entity_id: ENTITY_ID,
        pos: tuple[float, float],
        from_player_entity_id: ENTITY_ID,
        mass: float,
        angle: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.from_player_entity_id: ENTITY_ID = from_player_entity_id
        self.mass: float = mass
        self.angle: float = angle
