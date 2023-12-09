from models.entity import WorldEntity


class Blob(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: tuple[float, float],
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: tuple[float, float] = pos
        self.mass: float = mass
