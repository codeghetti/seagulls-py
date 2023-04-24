import pygame

from seagulls.cat_demos.app.environment._world_elements import WorldElement, WorldElementId, WorldElementIds
from seagulls.cat_demos.app.player._mouse_controls import MouseControlIds, MouseControls
from seagulls.cat_demos.app.player._player_controls import PlayerControlIds, PlayerControls
from seagulls.cat_demos.engine.v2.collisions._collider_component import RectCollider
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GameComponentConfig, GameObjectConfig, PrefabClient
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.debugging._debug_hud_prefab import DebugHud
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.frames._frames_client import Frame, FrameEvents
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId
from seagulls.cat_demos.engine.v2.text._text_component import Text
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class IndexScene(IExecutable):

    _prefab_client: PrefabClient
    _event_client: GameEventDispatcher
    _window_client: WindowClient

    def __init__(
        self,
        prefab_client: PrefabClient,
        event_client: GameEventDispatcher,
        window_client: WindowClient,
    ) -> None:
        self._prefab_client = prefab_client
        self._event_client = event_client
        self._window_client = window_client

    def __call__(self) -> None:
        #self._spawn_environment()
        self._spawn_sc_environment()
        #self._spawn_player()
        self._spawn_sc_player()
        self._spawn_sc_one_rock()
        self._spawn_menu()
        self._spawn_mouse()
        self._spawn_debug_hud()
        self._configure_events()

    def _spawn_environment(self):
        for x in range(15):
            for y in range(15):
                self._prefab_client.run(WorldElementIds.PREFAB, WorldElement(
                    object_id=GameObjectId(f"barrel::{x}.{y}"),
                    sprite_id=WorldElementId.BARREL,
                    position=Position(x=50 + (x * 32), y=50 + (y * 32)),
                ))

    def _spawn_sc_environment(self):
        self._prefab_client.run(WorldElementIds.PREFAB, WorldElement(
            object_id=GameObjectId(f"star_background"),
            sprite_id=WorldElementId.STAR_BACKGROUND,
            position=Position(x=0, y=0),
        ))

    def _spawn_sc_one_rock(self):
        self._prefab_client.run(WorldElementIds.PREFAB, WorldElement(
            object_id=GameObjectId(f"rock-large"),
            sprite_id=WorldElementId.ROCK_LARGE,
            position=Position(x=400, y=100),
        ))


    def _spawn_player(self):
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("player"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(200, 700),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("player")),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[RectCollider]("object-component::rect-collider"),
                    config=RectCollider(size=Size(width=16, height=16)),
                ),
            ),
        ))
        self._prefab_client.run(PlayerControlIds.PREFAB, PlayerControls(
            object_id=GameObjectId("player"),
            left_key=pygame.K_a,
            right_key=pygame.K_d,
            up_key=pygame.K_w,
            down_key=pygame.K_s,
        ))

    def _spawn_sc_player(self):
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("spaceship"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(500, 550),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("spaceship")),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[RectCollider]("object-component::rect-collider"),
                    config=RectCollider(size=Size(width=112, height=75)),
                ),
            ),
        ))
        self._prefab_client.run(PlayerControlIds.PREFAB, PlayerControls(
            object_id=GameObjectId("spaceship"),
            left_key=pygame.K_a,
            right_key=pygame.K_d,
            up_key=pygame.K_w,
            down_key=pygame.K_s,
        ))

    def _spawn_mouse(self) -> None:
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("mouse"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(0, 0),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("mouse")),
                ),
            ),
        ))
        self._prefab_client.run(MouseControlIds.PREFAB, MouseControls(object_id=GameObjectId("mouse")))

    def _spawn_menu(self) -> None:
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("menu:quit"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(600, 10),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("menu-button")),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Text]("object-component::text"),
                    config=Text(
                        value="Quit!",
                        font="monospace",
                        size=40,
                        color=Color(red=30, blue=30, green=30),
                    ),
                ),
            ),
        ))

    def _spawn_debug_hud(self) -> None:
        self._prefab_client.run(SessionComponents.DEBUG_HUD_PREFAB, DebugHud(show_fps=True))

    def _configure_events(self) -> None:
        def _on_frame() -> None:
            print("on frame?")
            self._window_client.get_surface().fill(Color(30, 30, 30))
        print("configuring on frame?")
        self._event_client.register(GameEventId[Frame](FrameEvents.OPEN), _on_frame)
