from enums.packet_type import PacketType
from game.models.client.client import Client
from helpers.java_data_stream import JavaDataOutputStream
from helpers.plugins import ScriptEvent
from packets.packet import Packet


class BattleRoyaleAction(Packet):
    def __init__(self, client: Client, do_register: bool) -> None:
        super().__init__(client, PacketType.BATTLE_ROYALE_ACTION)
        self.do_register: bool = do_register

    def write(self) -> bytes:
        self.data = (
            JavaDataOutputStream()
            .write_byte(self.packet_type.value)
            .write_int(self.client.server_data.cr2_token1)
            .write_byte(0x01 if self.do_register else 0x02)
            .get_data()
        )
        self.client.app.dispatch(ScriptEvent.PACKET_WRITE, self)
        return self.data
