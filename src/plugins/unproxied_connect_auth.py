from base.app import App
from game.sigs import APP_NAME_SIG, APP_VERSION_SIG
from helpers.plugins import Plugin
from requests import Response, post


class UnproxiedConnectAuth(Plugin):
    def __init__(self) -> None:
        super().__init__(
            name="UnproxiedConnectAuth",
            description="Authorize the client connection to the server",
            author="Discord: qxh",
        )

    @staticmethod
    def verify(client_auth_ticket: str | None = ",-") -> Exception | str:
        """Authorize the client's connection to the server.
        Do not spam this or you'll get a 500.
        This will return a base64-encoded string acting as a ticket
        for you to be able to connect.
        This must be passed with CONNECT_REQUEST_3
        """
        response: Response = post(
            "https://www.simplicialsoftware.com/api/account/JDKaYIIScQ",
            json={
                "Game": APP_NAME_SIG,
                "Version": str(APP_VERSION_SIG),
                "Ticket": client_auth_ticket,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status_code == 200:
            return response.json()["RezPlEVBeW"]
        return Exception(
            f"Failed to verify connection: {response.status_code} (are you spamming? Consider proxying your connection)"
        )


def setup(app: App) -> None:
    app.plugin_registry.register(UnproxiedConnectAuth())
