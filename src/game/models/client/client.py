from __future__ import annotations
from typing import TYPE_CHECKING
from game.models.client.client_data import ClientData
from game.models.client.wardrobe import Wardrobe
from game.models.client.control_data import ControlData


if TYPE_CHECKING:
    from base.app import App


class Client:
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.running: bool = False
        self.wardrobe: Wardrobe = Wardrobe()
        self.control_data: ControlData = ControlData()
        self.client_data: ClientData = ClientData()
