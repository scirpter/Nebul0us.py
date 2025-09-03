from game.models.entity import WorldEntity


class UndefinedJo(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        g: float,
        h: float,
        i: float,
        j: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.g: float = g
        self.h: float = h
        self.i: float = i
        self.j: float = j

    def update(self, g: float, h: float, i: float, j: float) -> None:
        self.g = g
        self.h = h
        self.i = i
        self.j = j
