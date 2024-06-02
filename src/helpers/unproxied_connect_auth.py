from time import sleep
from game.sigs import APP_NAME_SIG, APP_VERSION_SIG
from requests import Response, post


RETRY_DELAY_S = 2


class UnproxiedConnectAuth:
    @staticmethod
    def verify(
        client_auth_ticket: str | None = ",-", force_verify: bool = False
    ) -> Exception | str:
        """Authorize the client's connection to the server.
        Do not spam this or you'll get a 500.
        This will return a base64-encoded string acting as a ticket
        for you to be able to connect.
        This must be passed with CONNECT_REQUEST_3
        """
        while True:
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
            if force_verify:
                sleep(RETRY_DELAY_S)
                continue
            return Exception(
                f"Failed to verify connection: {response.status_code} (are you spamming? Consider proxying your connection)"
            )
