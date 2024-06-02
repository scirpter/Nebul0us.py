from base.custom_types import RELATIVE_ENTITY_ID
from game import enums
from game.models.entity import WorldEntity
from game.models.point import Point


class Item(WorldEntity):
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
        pos: Point,
        type: enums.ITEM_TYPE,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.type: enums.ITEM_TYPE = type
