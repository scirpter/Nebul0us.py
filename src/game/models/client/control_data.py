class ControlData:
    __speed: float = 0.0
    __angle: float = 0
    do_eject: bool = False
    do_split: bool = False
    do_item_drop: bool = False
    do_item_use: bool = False  # alias for eject

    __tick: int = 0x00

    @property
    def speed(self) -> float:
        """From 0.0 to 1.0"""
        return self.__speed

    @speed.setter
    def speed(self, value: float) -> None:
        self.__speed = value

    @property
    def tick(self) -> int:
        """From 0x00 to 0xFF. Increments by 1 every time a control packet is sent, resets to 0x00 after 0xFF"""
        return self.__tick

    @tick.setter
    def tick(self, value: int) -> None:
        self.__tick = value

    @property
    def angle(self) -> float:
        """From 0 to 2*PI.
        - Right: 0
        - Top right: 0.25*PI
        - Top left: 0.75*PI
        - Left: PI
        - Bottom left: 1.25*PI
        - Bottom right: 1.75*PI
        """
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        self.__angle = value

    def reset(self) -> None:
        self.__speed = 0.0
        self.__angle = 0.0
        self.do_eject = False
        self.do_split = False
        self.do_item_drop = False
        self.do_item_use = False
