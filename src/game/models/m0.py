from base.custom_types import RELATIVE_ENTITY_ID
from game.models.entity import WorldEntity


class UndefinedM0(WorldEntity):
    def __init__(self, d0: int, e0: int, f0: int) -> None:
        super().__init__(RELATIVE_ENTITY_ID(-1))
        self.d0: int = d0
        self.e0: int = e0
        self.f0: int = f0
