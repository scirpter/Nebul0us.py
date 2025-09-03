from __future__ import annotations
from game.models.client.client import Client
from typing import Any, Callable
import flet as ft
from helpers.config_integrity import (
    AppStates,
    PerClientSettings,
    ensure_integrity,
    ensure_client_config_integrity,
    get_default_client_settings,
    load_config,
)
from ui.components.notification import craft_notification


class App:
    page: ft.Page

    def __init__(self, devlogs_log_func: Callable[[str, str], None]) -> None:
        self.devlog: Callable[[str, str], None] = devlogs_log_func
        self.clients: list[Client] = []
        config: dict[str, Any] = load_config()
        ensure_integrity(config)

        self.states: AppStates = config  # type: ignore
        for setting in self.states["client_settings"]:
            client = Client(
                self,
                setting["client_uid"],
                setting["player_name"],
                setting["login_ticket"],
            )
            self.clients.append(client)
            client.setup_loops()

    def notify(self, title: str, description: str) -> None:
        # Create notification control
        n = craft_notification(
            title, description, self.states["cache"]["notifications"]
        )

        # Keep history for state, but append to the actual Column so Flet renders it
        self.states["cache"]["notifications"].append(n)
        self.states["cache"]["notification_column"].controls.append(n)  # type: ignore[index]

        # Update UI
        self.states["cache"]["notification_column"].update()  # type: ignore[index]
        self.states["cache"]["notification_container"].update()
        self.page.update()  # type: ignore

    def fetch_client_settings_from_uid(
        self, uid: int, name: str, ticket: str
    ) -> PerClientSettings:
        for settings in self.states["client_settings"]:
            if settings["client_uid"] == uid:
                return ensure_client_config_integrity(settings)

        default: PerClientSettings = get_default_client_settings(
            uid, name, ticket
        )

        self.states["client_settings"].append(default)
        return default
