import logging
from pygame import Surface, Vector2
from pygame.time import Clock
from seagulls.assets import AssetManager
from seagulls.pygame import GameObject
from seagulls.pygame._game_client import GameScene

logger = logging.getLogger(__name__)


class SimpleScene(GameScene):

    _asset_manager: AssetManager

    _unit: GameObject
    _clock: Clock

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager

        self._clock = Clock()

    def start(self) -> None:
        self._unit = GameObject(
            size=Vector2(64, 64),
            position=Vector2(0, 568),
            velocity=Vector2(1, 0),
            sprite=self._asset_manager.load_sprite("wizard/wizard1-stand"),
        )

        # Reset our clock
        self._clock.tick()

    def render(self, surface: Surface) -> None:
        self.update()
        background = self._get_background()
        radius = self._unit.size.x / 2
        blit_position = self._unit.position - Vector2(radius)
        background.blit(self._unit.sprite, (blit_position.x, blit_position.y))
        surface.blit(background, (0, 0))

    def update(self) -> None:
        tick = self._clock.tick()
        if self._unit.position.x > 790:
            self._unit.velocity = Vector2(-1, 0)
        elif self._unit.position.x < 10:
            self._unit.velocity = Vector2(1, 0)
        self._unit.update(tick)

    def _get_background(self) -> Surface:
        return self._asset_manager.load_sprite("environment/environment-sky")
