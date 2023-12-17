from base.custom_types import YetToBeDefined
from game.enums import SKIN, COLOR_CYCLE, FONT  # , Hat, Particle, EjectSkin


class Wardrobe:
    skin: SKIN | None = None
    color_cycle: COLOR_CYCLE | None = None
    name_font: FONT | None = None
    __halo: YetToBeDefined | None = None
    __hat: YetToBeDefined | None = None
    __particle: YetToBeDefined | None = None
    __eject_skin: YetToBeDefined | None = None

    @property
    def hat(self) -> YetToBeDefined | None:
        """default: 0xFF"""
        return self.__hat

    @hat.setter
    def hat(self, value: YetToBeDefined | None) -> None:
        self.__hat = value

    @property
    def halo(self) -> YetToBeDefined | None:
        """default: 0x00"""
        return self.__halo

    @halo.setter
    def halo(self, value: YetToBeDefined | None) -> None:
        self.__halo = value

    @property
    def particle(self) -> YetToBeDefined | None:
        """default: 0xFF"""
        return self.__particle

    @particle.setter
    def particle(self, value: YetToBeDefined | None) -> None:
        self.__particle = value

    @property
    def eject_skin(self) -> YetToBeDefined | None:
        """default: 0x00"""
        return self.__eject_skin
