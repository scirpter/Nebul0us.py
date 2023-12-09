from __future__ import annotations
from typing import Any, Callable

from helpers.plugins import ScriptEvent


class EventHandler:
    def __init__(self) -> None:
        self.event_handlers: dict[ScriptEvent, list[Callable[..., Any]]] = {}

    def register(self, t: ScriptEvent, callback: Callable[..., Any]) -> None:
        if t not in self.event_handlers:
            self.event_handlers[t] = []
        self.event_handlers[t].append(callback)

    def unregister(self, t: ScriptEvent, callback: Callable[..., Any]) -> None:
        if t not in self.event_handlers:
            return
        self.event_handlers[t].remove(callback)
