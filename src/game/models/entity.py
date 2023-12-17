from base.custom_types import ENTITY_ID


class WorldEntity:
    def __init__(
        self,
        relative_entity_id: ENTITY_ID,
    ) -> None:
        self.relative_entity_id: ENTITY_ID = relative_entity_id
