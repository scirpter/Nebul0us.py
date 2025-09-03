from game import enums
from game.models.entity import WorldEntity
from game.models.point import Point


class Item(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: Point,
        type: enums.ITEM_TYPE,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.type: enums.ITEM_TYPE = type

    def update(self, pos: Point, type: enums.ITEM_TYPE) -> None:
        self.pos = pos
        self.type = type
