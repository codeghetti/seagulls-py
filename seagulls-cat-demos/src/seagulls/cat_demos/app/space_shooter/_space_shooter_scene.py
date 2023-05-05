import pygame

from seagulls.cat_demos.app.environment._world_elements import (
    WorldElement,
    WorldElementClient, WorldElementId
)
from seagulls.cat_demos.app.player._mouse_controls import (
    MouseControlClient
)
from seagulls.cat_demos.app.player._player_controls import (
    PlayerControlClient, PlayerControls
)
from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    RectCollider, SelectionLayerId, SelectionLayers
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.debugging._debug_hud_client import DebugHud, DebugHudClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    Sprite,
    SpriteId
)
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class SpaceShooterScene(IExecutable):
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher
    _window_client: WindowClient
    _world_elements: WorldElementClient
    _mouse_controls: MouseControlClient
    _player_controls: PlayerControlClient
    _debug_hud: DebugHudClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
        window_client: WindowClient,
        world_elements: WorldElementClient,
        mouse_controls: MouseControlClient,
        player_controls: PlayerControlClient,
        debug_hud: DebugHudClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client
        self._window_client = window_client
        self._world_elements = world_elements
        self._mouse_controls = mouse_controls
        self._player_controls = player_controls
        self._debug_hud = debug_hud

    def __call__(self) -> None:
        self._spawn_environment()
        self._spawn_player()
        self._spawn_one_rock()
        self._spawn_debug_hud()

    def _spawn_environment(self):
        self._world_elements.spawn(WorldElement(
            object_id=GameObjectId("star_background"),
            sprite_id=WorldElementId.STAR_BACKGROUND,
            position=Position(x=0, y=0),
        ))

    def _spawn_one_rock(self) -> None:
        self._world_elements.spawn(WorldElement(
            object_id=GameObjectId("rock-large"),
            sprite_id=WorldElementId.ROCK_LARGE,
            position=Position(x=400, y=100),
        ))

    def _spawn_player(self) -> None:
        object_id = GameObjectId("spaceship")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(500, 550),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("spaceship"), layer="units"),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(
                size=Size(width=112, height=75),
                layers=SelectionLayers(
                    appears_in=frozenset({SelectionLayerId("buttons")}),
                    searches_in=frozenset({}),
                )),
        )

        self._player_controls.attach(PlayerControls(
            object_id=GameObjectId("spaceship"),
            left_key=pygame.K_a,
            right_key=pygame.K_d,
            up_key=pygame.K_w,
            down_key=pygame.K_s,
        ))

    def _spawn_debug_hud(self) -> None:
        self._debug_hud.execute(DebugHud(show_fps=True))
