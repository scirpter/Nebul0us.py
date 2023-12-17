from game.enums import PROFILE_VISIBILITY
from game.models.world import World


class ServerData:
    name: str
    login_ticket: str
    server_ip: str
    profile_visibility: PROFILE_VISIBILITY = PROFILE_VISIBILITY.APPEAR_OFFLINE
    is_idle: bool = False
    world: World = World()

    __cr2_token1: int
    __cr2_token2: int
    __rng_token1: int
    __rng_token2: int

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
