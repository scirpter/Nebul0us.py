from __future__ import annotations
from game.models.player import Player
from helpers._io.bytearray import ByteArray
from .packet import Packet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models.client.client import Client


class JOIN_RESULT(Packet):
    def __init__(self, client: Client, stream: bytes = b"") -> None:
        super().__init__(client, self, stream)
        self.__parse()

    def __parse(self) -> None:
        stream = ByteArray(self.stream)
        stream.read_byte()
        cr2_token2: int = stream.read_int()

        b6 = stream.read_byte()
        if b6 == 0:
            entity_id = stream.read_byte()
            player: Player | None = self.client.client_data.world.players.get(entity_id)
            if not player:
                player = Player(entity_id)
                self.client.client_data.world.players[entity_id] = player

            player.cr2_token2 = cr2_token2
            player.skin_id = stream.read_short()
            _some_unique = stream.read_int()
            _t = stream.read_byte()
            player.name = stream.read_utf()
            player.account_id = stream.read_int()
            player.xp = stream.read_long()
            _w = stream.read_utf()
            _z = stream.read_byte()
            _a = stream.read_int()
            _d = stream.read_bool()
            _m = stream.read_byte()
            _n = stream.read_int()
            # int i6 = c9370n0.readByte();
            # byte[] bArr = new byte[i6];
            # this.f27022i = bArr;
            # if (i6 > 16) {
            #     throw new RuntimeException("INVALID ALIAS COLORS LENGTH!");
            # }
            # c9370n0.readFully(bArr);
            # byte[] bArr2 = new byte[c9370n0.readByte()];
            # this.f27037x = bArr2;
            # c9370n0.readFully(bArr2);
            # byte b7 = c9370n0.readByte();
            # if (b7 < 0 || b7 >= 3) {
            #     b7 = 0;
            # }
            # this.f27003E = b7;
            # this.f27004F = c9370n0.readInt();
            # this.f27038y = C2231q.m4238d(c9370n0.readByte());
            # this.f27029p = c9370n0.readByte();
            # this.f27030q = c9370n0.readShort();
            # this.f27031r = c9370n0.readUTF();
            # this.f27005G = C2185L.m4136b(c9370n0.readByte());
            # this.f27007I = c9370n0.readInt();
            # this.f27006H = C2184K.m4134b(c9370n0.readByte());
            # this.f27008J = c9370n0.readByte();
            # this.f27009K = c9370n0.readShort();
            # this.f27010L = c9370n0.readUTF();
            # this.f27011M = c9370n0.readInt();
            # this.f27012N = c9370n0.readInt();
            # this.f27013O = c9370n0.readInt();
            # this.f27014P = C2196X.m4165a(c9370n0.readByte());
            # this.f27020g = C2190Q.m4143s(c9370n0.readByte());
            # c9370n0.readByte();
            # this.f27021h = AbstractC2242v0.m4482f(c9370n0.readByte());
            # this.f27024k = C2209f.m4208b(c9370n0.readShort());
            # this.f27025l = c9370n0.m10967f(60.0f);
            # this.f27028o = c9370n0.readInt();
            # byte[] bArr3 = new byte[c9370n0.readByte()];
            # this.f27015Q = bArr3;
            # c9370n0.readFully(bArr3);
            # this.f27000B = c9370n0.readByte();
            # this.f27001C = c9370n0.m10966e();
