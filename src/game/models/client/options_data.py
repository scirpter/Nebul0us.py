class OptionsData:
    def __init__(
        self,
        *,
        chase_nearest_holes: bool = True,
        auto_respawn: bool = True,
    ) -> None:
        self.chase_nearest_holes: bool = chase_nearest_holes
        self.auto_respawn: bool = auto_respawn
