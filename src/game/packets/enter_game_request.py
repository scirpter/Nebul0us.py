from game.sigs import APP_VERSION_SIG

from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from .packet import Packet


class ENTER_GAME_REQUEST(Packet):
    """Enables the client to join via account ID (requires the target account to appear as ONLINE, does not require friendship though)
    or join any hidden/public room via room password/name"""

    def __init__(
        self, client: Client, account_id: int | None = None, room_sig: str | None = None
    ) -> None:
        super().__init__(client, self)
        self.account_id: int = account_id or -1
        self.room_sig: str = room_sig or ""

        if self.account_id != -1 and self.room_sig != "":
            raise ValueError(
                f"Cannot specify both account_id and room_sig in {self.__class__.__name__}"
            )

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.client_data.cr2_token1)
            .write_int(self.client.client_data.rng_token1)
            .write_int(0xFFFFFFFF)
            .write_utf(self.room_sig)
            .write_int(self.account_id)
            .write_byte(0xFF)
            .write_short(APP_VERSION_SIG)
            .get_stream()
        )

        return self.stream
