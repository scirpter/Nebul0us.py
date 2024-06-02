from game.enums import PROFILE_VISIBILITY
from game.enums.server import Server
from game.models.world import VisibleWorld


class ClientData:
    def __init__(self) -> None:
        self.name: str = "NULL"
        self.login_ticket: str = ",-"
        self.server: Server = Server.EUROPE
        self.profile_visibility: PROFILE_VISIBILITY = PROFILE_VISIBILITY.APPEAR_OFFLINE
        self.is_idle: bool = False
        self.world: VisibleWorld = VisibleWorld()

        self.__cr2_token1: int = 0
        self.__cr2_token2: int = 0
        self.__rng_token1: int = 0
        self.__rng_token2: int = 0

    @property
    def cr2_token1(self) -> int:
        """Server-side client identification token (1).
        Received from CONNECT_RESULT_2"""
        return self.__cr2_token1

    @cr2_token1.setter
    def cr2_token1(self, value: int) -> None:
        self.__cr2_token1 = value

    @property
    def cr2_token2(self) -> int:
        """Server-side client identification token (2).
        Received from CONNECT_RESULT_2"""
        return self.__cr2_token2

    @cr2_token2.setter
    def cr2_token2(self, value: int) -> None:
        self.__cr2_token2 = value

    @property
    def rng_token1(self) -> int:
        """Randomized server-side client identification token (1).
        This is randomly generated client-side"""
        return self.__rng_token1

    @rng_token1.setter
    def rng_token1(self, value: int) -> None:
        self.__rng_token1 = value

    @property
    def rng_token2(self) -> int:
        """Randomized server-side client identification token (2).
        This is randomly generated client-side"""
        return self.__rng_token2

    @rng_token2.setter
    def rng_token2(self, value: int) -> None:
        self.__rng_token2 = value
