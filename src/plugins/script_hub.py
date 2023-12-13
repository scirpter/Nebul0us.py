from base.app import App
from helpers.plugins import (
    OptionalArg,
    Plugin,
    install_plugin,
    on,
    ScriptEvent,
    uninstall_plugin,
    RequiredArg,
)
import logging


class ScriptHub(Plugin):
    def __init__(self) -> None:
        super().__init__(
            name="ScriptHub",
            description="Manage your plugins",
            author="Discord: qxh",
            prefixes=["pi", "install"],
            arguments=[
                RequiredArg("msg_id"),
                RequiredArg("plugin_name"),
                OptionalArg("uninstall? y or n (default: n)"),
            ],
        )

    @on(ScriptEvent.CALLBACK)
    def run(self, msg_id: int, plugin_name: str, uninstall: str | None = "n") -> None:
        if uninstall == "n":
            code: int = install_plugin(plugin_name, msg_id)
            if code == 200:
                logging.info(f"Successfully installed {plugin_name}")
            else:
                logging.error(
                    f"Plugin {plugin_name} does not exist. Are you entering the ID and name correctly?"
                )
            return

        elif uninstall == "y":
            success, err = uninstall_plugin(plugin_name)
            if success:
                logging.info(f"Successfully uninstalled {plugin_name}")
            else:
                logging.error(err)

        else:
            logging.error("Invalid argument for uninstall. Expected y or n")


def setup(app: App) -> None:
    app.plugin_registry.register(ScriptHub())
