import logging

from seagulls.engine import GameClock, GameControls
from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    Camera,
    IPrinter,
    Position,
    SpriteClient,
    SpritesType
)
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

logger = logging.getLogger(__name__)


class Sprites(SpritesType):
    floor_left_corner = "floor-left-corner"
    floor_middle = "floor-middle"
    floor_right_corner = "floor-right-corner"
    pumpkin = "pumpkin"


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrinter
    _camera: Camera

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface,
            camera: Camera,
            sprite_client: SpriteClient,
            game_controls: GameControls,
            clock: GameClock):
        self._session = session
        self._printer = printer
        self._window = window
        self._camera = camera
        self._sprite_client = sprite_client
        self._game_controls = game_controls
        self._clock = clock
        self._pumpkin_position = 10
        self._counter = 1

    def tick(self) -> None:
        self._printer.clear()
        self._game_controls.tick()
        self._clock.tick()
        delta = self._clock.get_time()

        self._sprite_client.render_sprite(
            Sprites.floor_left_corner,
            Position({"x": 0, "y": 550})
        )

        for x in range(int(900/50)):
            self._sprite_client.render_sprite(
                Sprites.floor_middle,
                Position({"x": 50+x*50, "y": 550})
            )

        self._sprite_client.render_sprite(
            Sprites.floor_right_corner,
            Position({"x": 950, "y": 550})
        )

        if self._game_controls.is_right_moving() and self._pumpkin_position <= 955:
            self._pumpkin_position += int(10 * delta / 25)

        elif self._game_controls.is_left_moving() and self._pumpkin_position > 5:
            self._pumpkin_position -= int(10 * delta / 25)

        self._sprite_client.render_sprite(
            Sprites.pumpkin,
            Position({"x": self._pumpkin_position, "y": 515})
        )

        self._printer.commit()


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
