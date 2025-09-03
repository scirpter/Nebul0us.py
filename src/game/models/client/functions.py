from __future__ import annotations
from typing import TYPE_CHECKING
import math
from game.models.hole import Hole
from game.models.player import Player
from game.models.point import Point


if TYPE_CHECKING:
    from game.models.client.client import Client


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def angle_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.atan2(delta_y, delta_x)


def functions(client: Client, player: Player, avg_pos: Point) -> None:
    """tasks executed on every control tick"""

    if client.options_data.chase_nearest_holes:
        holes: list[Hole] = Hole.combine_data(client.app.clients)
        if holes:
            distances = [
                distance(avg_pos.x, avg_pos.y, hole.pos.x, hole.pos.y)
                for hole in holes
                if not hole.is_dead()
            ]
            if distances:
                min_distance = min(distances)
                closest_hole = holes[distances.index(min_distance)]
                angle = angle_between_points(
                    avg_pos.x, avg_pos.y, closest_hole.pos.x, closest_hole.pos.y
                )
                client.control_data.angle = angle
                client.control_data.speed = 1.0
                client.control_data.do_split = True
            else:
                client.control_data.reset()
        else:
            client.control_data.reset()
    else:
        client.control_data.reset()
