import pygame
from pygame.font import Font

from seagulls.cat_demos.app.player._mouse_controls import MouseControlIds, MouseControls
from seagulls.cat_demos.app.player._player_controls import PlayerControlIds, PlayerControls
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GameComponentConfig, GameObjectConfig, PrefabClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEventDispatcher
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId
from seagulls.cat_demos.engine.v2.text._text_component import Text


class IndexScene(IExecutable):

    _prefab_client: PrefabClient
    _event_client: GameEventDispatcher

    def __init__(
        self,
        prefab_client: PrefabClient,
        event_client: GameEventDispatcher,
    ) -> None:
        self._prefab_client = prefab_client
        self._event_client = event_client

    def __call__(self) -> None:
        self._spawn_player()
        self._spawn_menu()
        self._spawn_mouse()
        self._configure_events()

    def _spawn_welcome_text(self):
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("welcome-text"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(10, 10),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Text]("object-component::text"),
                    config=Text(
                        value="hello, fancy pants!",
                        font=GameComponentId[Font]("font.default"),
                        size=5,
                        color=Color(red=200, green=150, blue=150),
                    ),
                ),
            ),
        ))

    def _spawn_player(self):
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("player"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(10, 600),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("player")),
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
                    config=Position(100, 100),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("menu-button")),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Text]("object-component::text"),
                    config=Text(
                        value="Quit",
                        font=GameComponentId("default"),
                        size=11,
                        color=Color(red=200, blue=200, green=200),
                    ),
                ),
            ),
        ))

    def _configure_events(self) -> None:
        pass
