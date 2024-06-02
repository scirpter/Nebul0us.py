from __future__ import annotations
from base.gowire import Gowire
from game.models.client.client import Client
from typing import Any
import flet as ft
from helpers.config_integrity import AppStatery, ensure_integrity, load_config
from ui.components.notification import craft_notification


class App:
    page: ft.Page

    def __init__(self) -> None:
        self.wire: Gowire = Gowire()
        self.clients: list[Client] = []

        config: dict[str, Any] = load_config()
        ensure_integrity(config)

        self.statery: AppStatery = config  # type: ignore

    def notify(self, title: str, description: str) -> None:
        self.statery["notifications"].append(
            craft_notification(title, description, self.statery["notifications"])
        )
        self.statery["notification_container"].update()
