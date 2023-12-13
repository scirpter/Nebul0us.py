from __future__ import annotations
from types import ModuleType
from typing import Any, Callable, Optional
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
                    if hasattr(func, "event") and func.event == t:  # type: ignore
                        args_no_prefix: list[Any] = list(args[1:])

                        annotations: dict[str, Any] = func.__annotations__
                        if "return" in annotations:
                            annotations.pop("return")

                        optional_ct: int = 0
                        for _, arg_type in annotations.copy().items():
                            if arg_type == Optional[arg_type]:
                                optional_ct += 1

                        # check if the number of arguments is correct
                        if len(annotations) - optional_ct > len(args_no_prefix):
                            logging.error(
                                f"Not enough arguments were passed. Expected {len(annotations)-optional_ct}{f'-{len(annotations)}' if optional_ct else ''} but got {len(args_no_prefix)}. Here's how to use the command properly: {plugin_prefix} {plugin.usage}"
                            )
                            continue

                        # too many arguments in args_no_prefix
                        elif len(annotations) < len(args_no_prefix):
                            logging.error(
                                f"Too many arguments were passed. Expected {len(annotations)-optional_ct}{f'-{len(annotations)}' if optional_ct else ''} but got {len(args_no_prefix)}. Here's how to use the command properly: {plugin_prefix} {plugin.usage}"
                            )
                            continue

                        # enforce proper types
                        for i, arg_type in enumerate(args_no_prefix):
                            # arg_name: str = list(annotations.keys())[i]
                            # arg_usage: str = plugin.arguments[i].arg
                            required_type: Any = list(annotations.values())[i]
                            if not isinstance(arg_type, required_type):
                                # try forcing the type
                                try:
                                    args_no_prefix[i] = required_type(arg_type)
                                except Exception:
                                    logging.error(
                                        f"Argument {i+1} is not of type {required_type}. Here's how to use the command properly: {plugin_prefix} {plugin.usage}"
                                    )
                                    return

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
