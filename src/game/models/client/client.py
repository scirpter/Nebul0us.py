from __future__ import annotations
from typing import TYPE_CHECKING
from game.models.client import Wardrobe, ControlData, ServerData


if TYPE_CHECKING:
    from base.app import App


class Client:
    def __init__(self, app: App) -> None:
        self.app: App = app

        self.wardrobe: Wardrobe = Wardrobe()
        self.control_data: ControlData = ControlData()
        self.server_data: ServerData = ServerData()
