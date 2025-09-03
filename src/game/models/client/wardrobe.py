from game.enums import SKIN, COLOR_CYCLE, FONT  # , Hat, Particle, EjectSkin


class Wardrobe:
    def __init__(self) -> None:
        self.skin: SKIN = SKIN.misc_none
        self.color_cycle: COLOR_CYCLE = COLOR_CYCLE.NONE
        self.name_font: FONT = FONT.DEFAULT
        self._halo: int | None = None
        self._hat: int | None = None
        self._particle: int | None = None
        self._eject_skin: int | None = None

    @property
    def hat(self) -> int | None:
        """default: 0xFF"""
        return self._hat

    @hat.setter
    def hat(self, value: int | None) -> None:
        self._hat = value

    @property
    def halo(self) -> int | None:
        """default: 0x00"""
        return self._halo

    @halo.setter
    def halo(self, value: int | None) -> None:
        self._halo = value

    @property
    def particle(self) -> int | None:
        """default: 0xFF"""
        return self._particle

    @particle.setter
    def particle(self, value: int | None) -> None:
        self._particle = value

    @property
    def eject_skin(self) -> int | None:
        """default: 0x00"""
        return self._eject_skin
