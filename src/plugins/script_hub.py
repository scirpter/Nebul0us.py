from base.app import App
from helpers.plugins import Plugin, install_plugin, on, ScriptEvent, uninstall_plugin
import logging


class ScriptHub(Plugin):
    def __init__(self) -> None:
        super().__init__(
            name="ScriptHub",
            description="Manage your plugins",
            author="Discord: qxh",
            prefixes=["pi", "install"],
            arguments=["<msg_id>", "<plugin_name>", "[uninstall? y or n (default: n)]"],
        )

    @on(ScriptEvent.CALLBACK)
    def run(self, msg_id: int, plugin_name: str, uninstall: str = "n") -> None:
        if uninstall == "n":
            code: int = install_plugin(plugin_name, msg_id)
            if code == 200:
                logging.info(f"Successfully installed {plugin_name}")
            else:
                logging.error(
                    f"Plugin {plugin_name} does not exist. Are you entering the ID and name correctly?"
                )
            return

        success, err = uninstall_plugin(plugin_name)
        if success:
            logging.info(f"Successfully uninstalled {plugin_name}")
        else:
            logging.error(err)


def setup(app: App) -> None:
    app.plugin_registry.register(ScriptHub())
