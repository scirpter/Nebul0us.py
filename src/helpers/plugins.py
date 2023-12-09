from __future__ import annotations
from typing import Any, Callable
from enum import Enum, auto


def on(s: ScriptEvent) -> Callable[..., Any]:
    def decorator(fun: Callable[..., Any]) -> Callable[..., Any]:
        if not fun.events:  # type: ignore
            fun.events: list[ScriptEvent] = []  # type: ignore
        fun.events.append(s)  # type: ignore
        return fun

    return decorator


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


class Plugin:
    __instance: Plugin | None = None

    def __init__(
        self,
        *,
        name: str,
        description: str,
        author: str,
        prefixes: list[str] | None = None,
        arguments: list[str] | None = None,
        dependencies: list[Dependency] | None = None,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.author: str = author
        self.prefixes: list[str] = prefixes or []
        self.arguments: list[str] = arguments or []
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
        return " OR ".join(self.prefixes) + " " + " ".join(self.arguments)

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
        # list all plugin functions
        self.plugins.append(plugin)
