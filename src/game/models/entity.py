from base.custom_types import RELATIVE_ENTITY_ID
from abc import ABC, abstractmethod


class WorldEntity(ABC):
    @abstractmethod
    def __init__(
        self,
        relative_entity_id: RELATIVE_ENTITY_ID,
    ) -> None:
        self.relative_entity_id: RELATIVE_ENTITY_ID = relative_entity_id
