from __future__ import annotations
from types import ModuleType
from typing import Any, Callable
from base.event_handler import EventHandler, ScriptEvent
from base.gowire import Gowire
from helpers.plugins import PluginRegistry
from game.models.client import Client
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path


class App:
    def __init__(self) -> None:
        self.wire: Gowire = Gowire()
        self.plugin_registry: PluginRegistry = PluginRegistry()
        self.event_handler: EventHandler = EventHandler()
        self.clients: list[Client] = []

    def dispatch(self, t: ScriptEvent, *args: ..., **kwargs: ...) -> None:  # type: ignore
        if t not in self.event_handler.event_handlers:
            return
        for callback in self.event_handler.event_handlers[t]:
            callback(*args, **kwargs)

    def on(self, t: ScriptEvent, fun: Callable[..., Any]) -> App:
        self.event_handler.register(t, fun)
        return self

    def register_plugins(self) -> App:
        for path in Path("src/plugins").iterdir():
            if not path.name.endswith(".py") and path.name.startswith("_"):
                continue
            module: ModuleType = import_module(f".{path.stem}", "plugins")
            if find_spec(f"plugins.{path.stem}"):
                _setup: Callable[..., Any] | Any = getattr(module, "setup", None)
                if callable(_setup):
                    _setup(self)
        return self
