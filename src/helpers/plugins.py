from __future__ import annotations
import logging
from typing import Any, Callable
from enum import Enum, auto
from requests import Response, get
from pathlib import Path


PLUGIN_CHANNEL_ID = 1179542458749685770


def on(s: ScriptEvent) -> Callable[..., Any]:
    def decorator(fun: Callable[..., Any]) -> Callable[..., Any]:
        annotations: dict[str, Any] = fun.__annotations__
        if "return" in annotations:
            annotations.pop("return")
        if fun.__code__.co_argcount < len(annotations):
            logging.warning(
                f"Plugin callback {fun.__qualname__} could not be registered: please use parameter type hints (return type is optional)"
            )
            return fun

        if not hasattr(fun, "event"):
            fun.event: ScriptEvent = s  # type: ignore
            logging.info(f"Registered {fun.__qualname__} for {s.name}")
        else:
            logging.warning(
                f"Plugin {fun.__qualname__} could not be registered as {s.name}: already registered as {fun.event.name}"  # type: ignore
            )
        return fun

    return decorator


def install_plugin(plugin_name: str, msg_id: int) -> int:
    """Returns the response code of the request"""
    response: Response = get(
        f"https://cdn.discordapp.com/attachments/{PLUGIN_CHANNEL_ID}/{msg_id}/{plugin_name}.py"
    )
    if response.status_code != 200:
        return response.status_code

    with open(f"src/plugins/{plugin_name}.py", "w") as f:
        f.write(response.text)

    return response.status_code


def uninstall_plugin(plugin_name: str) -> tuple[bool, Exception | None]:
    try:
        Path(f"src/plugins/{plugin_name}.py").unlink()
        return (True, None)
    except FileNotFoundError:
        return (False, FileNotFoundError(f"Plugin {plugin_name} is not installed"))


class ScriptEvent(Enum):
    CALLBACK = auto()
    TICK = auto()
    PACKET_SEND = auto()
    PACKET_READ = auto()
    PACKET_WRITE = auto()
    PACKET_RECEIVE = auto()


class Dependency:
    def __init__(self, plugin_name: str, msg_id: int) -> None:
        self.plugin_name: str = plugin_name
        self.msg_id: int = msg_id


class OptionalArg:
    def __init__(self, arg: str) -> None:
        self.arg: Any = arg


class RequiredArg:
    def __init__(self, arg: str) -> None:
        self.arg: Any = arg


class Plugin:
    __instance: Plugin | None = None

    def __init__(
        self,
        *,
        name: str,
        description: str,
        author: str,
        prefixes: list[str] | None = None,
        arguments: list[RequiredArg | OptionalArg] | None = None,
        dependencies: list[Dependency] | None = None,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.author: str = author
        self.prefixes: list[str] = prefixes or []
        self.arguments: list[RequiredArg | OptionalArg] = arguments or []
        self.dependencies: list[Dependency] = dependencies or []
        self.__dependency_locked: bool = True
        self.__instance: Plugin | None = self

    @classmethod
    def get_instance(cls) -> Plugin | None:
        """Get the class instance of the plugin.
        A plugin is a singleton, so it will return the only existing instance.

        ```code
        >>> t1 = Template(app)
        >>> t2 = Template.get_instance()
        >>> t1 == t2
        True
        ```"""
        return cls.__instance

    @property
    def usage(self) -> str:
        """Help the user understand how to use the plugin properly"""
        return " ".join(
            [
                f"<{arg.arg}>" if isinstance(arg, RequiredArg) else f"({arg.arg})"
                for arg in self.arguments
            ]
        )

    @property
    def dependency_locked(self) -> bool:
        """Whether the plugin has all dependencies installed.
        If this stays True, the user did not agree on installing the dependencies and the plugin will not work
        """
        return self.__dependency_locked

    def ensure_dependencies(self) -> None:
        ...  # TODO: finish this


class PluginRegistry:
    def __init__(self) -> None:
        self.plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        if plugin in self.plugins:
            return

        self.plugins.append(plugin)

    def unregister(self, plugin: Plugin) -> None:
        if plugin not in self.plugins:
            return

        self.plugins.remove(plugin)
