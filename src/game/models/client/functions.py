from __future__ import annotations
from typing import TYPE_CHECKING
from game.models.player import Player
from game.models.point import Point
from helpers.common import distance


if TYPE_CHECKING:
    from game.models.client.client import Client


def functions(client: Client, player: Player, avg_pos: Point) -> None:
    """Tasks executed on every control tick"""

    # Build observation
    world = client.client_data.world
    # Reference position: our largest blob if present, else average position
    my_ref = player.get_blob_sorted(0)
    my_pos = my_ref.pos if my_ref else avg_pos

    if client.options_data.chase_nearest_holes:
        holes = [h for h in world.holes.copy().values() if h.is_present()]
        if not client.options_data.chase_nearest_holes or not holes:
            client.control_data.reset()
            return

        target = min(
            holes,
            key=lambda hole: distance(
                my_pos.x, my_pos.y, hole.pos.x, hole.pos.y
            ),
        )
        client.move_towards(
            target.pos.x, target.pos.y, my_pos.x, my_pos.y, split=True
        )
