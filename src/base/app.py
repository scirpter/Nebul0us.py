from __future__ import annotations
from types import ModuleType
from typing import Any, Callable
from base.gowire import Gowire
from helpers.plugins import PluginRegistry, ScriptEvent
from game.models.client import Client
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path


class App:
    def __init__(self) -> None:
        self.wire: Gowire = Gowire()
        self.plugin_registry: PluginRegistry = PluginRegistry()
        self.clients: list[Client] = []

    def dispatch(self, t: ScriptEvent, *args: ..., **kwargs: ...) -> None:  # type: ignore
        ...

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
