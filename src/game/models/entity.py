from base.custom_types import EntityId


class WorldEntity:
    def __init__(
        self,
        relative_entity_id: EntityId,
    ) -> None:
        self.relative_entity_id: EntityId = relative_entity_id
