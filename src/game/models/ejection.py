from models.entity import WorldEntity


class Ejection(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: tuple[float, float],
        from_player_relative_entity_id: int,
        mass: float,
        angle: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.from_player_relative_entity_id: int = from_player_relative_entity_id
        self.mass: float = mass
        self.angle: float = angle
