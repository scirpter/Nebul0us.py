from __future__ import annotations
from game.enums.hole_type import HOLE_TYPE
from game.models.entity import WorldEntity
from game.models.point import Point
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.models.client.client import Client


class Hole(WorldEntity):
    def __init__(
        self,
        relative_entity_id: int,
        pos: Point,
        type: HOLE_TYPE,
        mass: float,
    ) -> None:
        super().__init__(relative_entity_id)
        self.pos: Point = pos
        self.type: HOLE_TYPE = type
        self.mass: float = mass

    def update(self, pos: Point, type: HOLE_TYPE, mass: float) -> None:
        self.pos = pos
        self.type = type
        self.mass = mass

    def is_dead(self) -> bool:
        return self.mass == 0

    @staticmethod
    def combine_data(all_clients: list[Client]) -> list[Hole]:
        combined_holes: dict[int, Hole] = {}
        for client in all_clients:
            for hole in client.client_data.world.holes.copy().values():
                if hole.relative_entity_id not in combined_holes:
                    combined_holes[hole.relative_entity_id] = hole
                else:
                    existing_hole = combined_holes[hole.relative_entity_id]
                    if hole.mass > existing_hole.mass:
                        combined_holes[hole.relative_entity_id] = hole
        return list(combined_holes.values())
