from seagulls.rendering import IGameScreen, IProvideGameScreens


class ScreenProvider(IProvideGameScreens):

    def __init__(self, screen: IGameScreen):
        self._screen = screen

    def get(self) -> IGameScreen:
        return self._screen
