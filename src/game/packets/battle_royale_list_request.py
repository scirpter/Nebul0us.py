from helpers.plugins import ScriptEvent
from enums.packet_type import PACKET_TYPE
from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from packets.packet import Packet


class BATTLE_ROYALE_LIST_REQUEST(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, PACKET_TYPE.BATTLE_ROYALE_LIST_REQUEST)

    def write(self) -> bytes:
        self.stream = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.server_data.cr2_token1)
            .write_int(self.client.server_data.rng_token1)
            .get_stream()
        )
        self.client.app.dispatch(ScriptEvent.PACKET_WRITE, self)
        return self.stream
