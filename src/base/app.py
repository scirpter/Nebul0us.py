from __future__ import annotations
from types import ModuleType
from typing import Any, Callable
from base.gowire import Gowire
from helpers.plugins import PluginRegistry, ScriptEvent
from game.models.client.client import Client
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
import logging
import inspect


class App:
    def __init__(self) -> None:
        self.wire: Gowire = Gowire()
        self.plugin_registry: PluginRegistry = PluginRegistry()
        self.clients: list[Client] = []

    def dispatch(self, t: ScriptEvent, *args: ..., **kwargs: ...) -> None:  # type: ignore
        if t == ScriptEvent.CALLBACK:
            plugin_prefix: str = args[0]

            for plugin in self.plugin_registry.plugins:
                if plugin_prefix not in plugin.prefixes:
                    continue

                # get the callback function by looping over all the functions in the plugin. the function that is the callback has the attribute "callback = True"
                for _name, func in inspect.getmembers(
                    plugin, predicate=inspect.ismethod
                ):
                    if hasattr(func, "events") and t in func.events:  # type: ignore
                        args_no_prefix: list[Any] = list(args[1:])
                        func(*args_no_prefix)

    def register_plugins(self) -> App:
        for path in Path("src/plugins").iterdir():
            if not path.name.endswith(".py") and path.name.startswith("_"):
                continue
            module: ModuleType = import_module(f".{path.stem}", "plugins")
            if find_spec(f"plugins.{path.stem}"):
                _setup: Callable[..., Any] | Any = getattr(module, "setup", None)
                if callable(_setup):
                    _setup(self)

        logging.info("Successfully registered plugins")
        return self
