from abc import ABC, abstractmethod


class WorldEntity(ABC):
    @abstractmethod
    def __init__(
        self,
        relative_entity_id: int,
    ) -> None:
        self.relative_entity_id: int = relative_entity_id
