from base.app import App
from helpers.plugins import Plugin, Dependency, ScriptEvent, on

try:
    from plugins.unproxied_connect_auth import UnproxiedConnectAuth
except ImportError:
    ...


class ServerConnector(Plugin):
    def __init__(self) -> None:
        super().__init__(
            name="ServerConnector",
            description="Send CONNECT_REQUEST_3 to the server",
            author="Discord: qxh",
            dependencies=[Dependency("unproxied_connect_auth", 0xDEADBEEF)],
        )

    @on(ScriptEvent.CALLBACK)
    def run(self) -> None:
        auth_token: Exception | str = UnproxiedConnectAuth.verify(",-")
        ...  # TODO: send CONNECT_REQUEST_3


def setup(app: App) -> None:
    app.plugin_registry.register(ServerConnector())
