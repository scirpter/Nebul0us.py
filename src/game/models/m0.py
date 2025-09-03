from game.models.entity import WorldEntity


class UndefinedM0(WorldEntity):
    def __init__(self, d0: int, e0: int, f0: int) -> None:
        super().__init__(-1)
        self.d0: int = d0
        self.e0: int = e0
        self.f0: int = f0

    def update(self, d0: int, e0: int, f0: int) -> None:
        self.d0 = d0
        self.e0 = e0
        self.f0 = f0
