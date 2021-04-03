import logging
from seagulls.assets import AssetManager
from seagulls.pygame import (
    GameTimeProvider,
    Vector2,
    Surface, GameControls,
)

logger = logging.getLogger(__name__)


class SimpleWizard:

    _clock: GameTimeProvider
    _sprite: Surface
    _controls: GameControls

    _size: Vector2
    _position: Vector2
    _velocity: Vector2

    def __init__(self, clock: GameTimeProvider, sprite: Surface, controls: GameControls):
        self._clock = clock
        self._sprite = sprite
        self._controls = controls

        self._size = Vector2(64, 64)
        self._position = Vector2(0, 568)
        self._velocity = Vector2(1, 0)

    def update(self) -> None:
        if self._position.x > 790:
            self._velocity = Vector2(-1, 0)
        elif self._position.x < 10:
            self._velocity = Vector2(1, 0)

        if self._controls.should_fire():
            logger.info("FIRING!")

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(self._sprite, (blit_position.x, blit_position.y))


class SimpleWizardFactory:
    _asset_manager: AssetManager
    _clock: GameTimeProvider
    _controls: GameControls

    def __init__(
            self,
            asset_manager: AssetManager,
            clock: GameTimeProvider,
            controls: GameControls):
        self._asset_manager = asset_manager
        self._clock = clock
        self._controls = controls

    def create(self) -> SimpleWizard:
        return SimpleWizard(
            clock=self._clock,
            sprite=self._asset_manager.load_sprite("wizard/wizard1-stand"),
            controls=self._controls,
        )
