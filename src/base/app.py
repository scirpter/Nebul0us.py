from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from queue import SimpleQueue
from typing import Any, Callable

from game.models.client.client import Client
from helpers.config_integrity import (
    AppStates,
    PerClientSettings,
    ensure_client_config_integrity,
    ensure_integrity,
    get_default_client_settings,
    load_config,
)


@dataclass(slots=True)
class Notification:
    title: str
    message: str


@dataclass(slots=True)
class DevLogEntry:
    message: str
    importance: str
    timestamp: datetime = field(default_factory=datetime.now)


class App:
    def __init__(self, devlog_hook: Callable[[str, str], None] | None = None) -> None:
        self._devlog_hook = devlog_hook
        self.clients: list[Client] = []
        config: dict[str, Any] = load_config()
        ensure_integrity(config)

        self.states: AppStates = config  # type: ignore[assignment]
        self.notifications: SimpleQueue[Notification] = SimpleQueue()
        self.devlog_entries: list[DevLogEntry] = []
        self.devlog_queue: SimpleQueue[DevLogEntry] = SimpleQueue()

        for setting in self.states["client_settings"]:
            client = Client(
                self,
                setting["client_uid"],
                setting["player_name"],
                setting["login_ticket"],
            )
            self.clients.append(client)
            client.setup_loops()

    def devlog(self, message: str, importance: str) -> None:
        entry = DevLogEntry(message=message, importance=importance)
        self.devlog_entries.append(entry)
        self.devlog_queue.put(entry)
        if self._devlog_hook:
            self._devlog_hook(message, importance)

    def notify(self, title: str, description: str) -> None:
        entry = Notification(title=title, message=description)
        self.notifications.put(entry)
        self.states["cache"]["notifications"].append(  # type: ignore[index]
            {"title": title, "message": description}
        )

    def fetch_client_settings_from_uid(
        self, uid: int, name: str, ticket: str
    ) -> PerClientSettings:
        for settings in self.states["client_settings"]:
            if settings["client_uid"] == uid:
                return ensure_client_config_integrity(settings)

        default: PerClientSettings = get_default_client_settings(uid, name, ticket)

        self.states["client_settings"].append(default)
        return default
