from base.app import App
from helpers.plugins import Plugin, on, ScriptEvent
from requests import Response, get


CHANNEL_ID = 1179542458749685770


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
            response: Response = get(
                f"https://cdn.discordapp.com/attachments/{CHANNEL_ID}/{msg_id}/{plugin_name}.py"
            )
            if response.status_code != 200:
                print(f"Failed to download plugin {plugin_name}")
                return

            with open(f"src/plugins/{plugin_name}.py", "w") as f:
                f.write(response.text)


def setup(app: App) -> None:
    app.plugin_registry.register(ScriptHub())
