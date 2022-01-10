from seagulls.engine import GameObject, Surface


class ToggleableGameObject(GameObject):
    _game_object: GameObject
    _active: bool

    def __init__(self, game_object: GameObject):
        self._game_object = game_object
        self._active = True

    def tick(self) -> None:
        if self._active:
            self._game_object.tick()

    def render(self, surface: Surface) -> None:
        if self._active:
            self._game_object.render(surface)

    def toggle(self) -> None:
        self._active = not self._active
