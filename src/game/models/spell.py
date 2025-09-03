from game.enums.spell_status import SPELL_STATUS
from game.enums.spell_type import SPELL_TYPE
from game.models.entity import WorldEntity
from game.models.point import Point


class Spell(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: Point,
        type_: SPELL_TYPE,
        status: SPELL_STATUS,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.type: SPELL_TYPE = type_
        self.status: SPELL_STATUS = status
