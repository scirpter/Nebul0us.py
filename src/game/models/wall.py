from game.models.entity import WorldEntity


class Wall(WorldEntity):

    def __init__(
        self,
        relative_entity_id: int,
        z: float,
        a0: float,
        b0: float,
        c0: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.z: float = z
        self.a0: float = a0
        self.b0: float = b0
        self.c0: float = c0

    def update(self, z: float, a0: float, b0: float, c0: float) -> None:
        self.z = z
        self.a0 = a0
        self.b0 = b0
        self.c0 = c0
