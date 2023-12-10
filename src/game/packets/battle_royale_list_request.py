from helpers.plugins import ScriptEvent
from enums.packet_type import PacketType
from helpers.java_data_stream import JavaDataOutputStream
from game.models.client.client import Client
from packets.packet import Packet


class BattleRoyaleListRequest(Packet):
    def __init__(self, client: Client) -> None:
        super().__init__(client, PacketType.BATTLE_ROYALE_LIST_REQUEST)

    def write(self) -> bytes:
        self.data = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.server_data.cr2_token1)
            .write_int(self.client.server_data.rng_token1)
            .get_data()
        )
        self.client.app.dispatch(ScriptEvent.PACKET_WRITE, self)
        return self.data
