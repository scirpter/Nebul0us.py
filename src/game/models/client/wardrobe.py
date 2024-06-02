from base.custom_types import YET_TO_BE_DEFINED
from game.enums import SKIN, COLOR_CYCLE, FONT  # , Hat, Particle, EjectSkin


class Wardrobe:
    skin: SKIN | None = None
    color_cycle: COLOR_CYCLE | None = None
    name_font: FONT | None = None
    __halo: YET_TO_BE_DEFINED | None = None
    __hat: YET_TO_BE_DEFINED | None = None
    __particle: YET_TO_BE_DEFINED | None = None
    __eject_skin: YET_TO_BE_DEFINED | None = None

    @property
    def hat(self) -> YET_TO_BE_DEFINED | None:
        """default: 0xFF"""
        return self.__hat

    @hat.setter
    def hat(self, value: YET_TO_BE_DEFINED | None) -> None:
        self.__hat = value

    @property
    def halo(self) -> YET_TO_BE_DEFINED | None:
        """default: 0x00"""
        return self.__halo

    @halo.setter
    def halo(self, value: YET_TO_BE_DEFINED | None) -> None:
        self.__halo = value

    @property
    def particle(self) -> YET_TO_BE_DEFINED | None:
        """default: 0xFF"""
        return self.__particle

    @particle.setter
    def particle(self, value: YET_TO_BE_DEFINED | None) -> None:
        self.__particle = value

    @property
    def eject_skin(self) -> YET_TO_BE_DEFINED | None:
        """default: 0x00"""
        return self.__eject_skin
