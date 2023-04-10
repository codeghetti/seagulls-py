import logging
from typing import NamedTuple, Tuple

import pygame
from pygame.font import Font

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId, GameSceneId
from seagulls.cat_demos.engine.v2.components._prefabs import GameComponentConfig, GameObjectConfig, PrefabClient
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.input._input_toggles import InputTogglesClient
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.scenes._client import SceneEvents
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId, SpriteSource
from seagulls.cat_demos.engine.v2.text._text_component import Text

logger = logging.getLogger(__name__)


class PlayerControls(NamedTuple):
    pass


class PlayerMoveEvent(NamedTuple):
    object_id: GameObjectId
    direction: Position


class PlayerControlsComponent(IExecutable):

    _objects: SceneObjects
    _event_provider: ServiceProvider[PlayerMoveEvent]

    def __init__(self, objects: SceneObjects, event_provider: ServiceProvider[PlayerMoveEvent]) -> None:
        self._objects = objects
        self._event_provider = event_provider

    def __call__(self) -> None:
        payload = self._event_provider()
        current_position = self._objects.get_component(
            entity_id=payload.object_id,
            component_id=GameComponentId[Position]("object-component::position"),
        )
        self._objects.set_component(
            entity_id=payload.object_id,
            component_id=GameComponentId[Position]("object-component::position"),
            config=current_position + payload.direction,
        )


class PlayerControlIds:
    MOVE_EVENT = GameEventId[PlayerMoveEvent]("player-controls.move")
    COMPONENT = GameComponentId[PlayerControlsComponent]("object-component::player-controls")


class OpenScene(IExecutable):

    _prefab_client: PrefabClient
    _event_client: GameEventDispatcher
    _player_controls: PlayerControlsComponent
    _toggles: InputTogglesClient

    def __init__(
        self,
        prefab_client: PrefabClient,
        event_client: GameEventDispatcher,
        player_controls: PlayerControlsComponent,
        toggles: InputTogglesClient,
    ) -> None:
        self._prefab_client = prefab_client
        self._event_client = event_client
        self._player_controls = player_controls
        self._toggles = toggles

    def __call__(self) -> None:
        self._spawn_player()
        self._spawn_welcome_text()
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
                GameComponentConfig(
                    component_id=GameComponentId[PlayerControls]("object-component::player-controls"),
                    config=PlayerControls(),
                ),
            ),
        ))

    def _configure_events(self) -> None:
        self._event_client.register(PygameEvents.key(pygame.K_a), self._on_keyboard)
        self._event_client.register(PygameEvents.key(pygame.K_s), self._on_keyboard)
        self._event_client.register(PygameEvents.key(pygame.K_d), self._on_keyboard)
        self._event_client.register(PygameEvents.key(pygame.K_w), self._on_keyboard)

        self._event_client.register(PlayerControlIds.MOVE_EVENT, self._player_controls)

    def _on_keyboard(self) -> None:
        mapping = {
            pygame.K_a: Position(-1, 0),
            pygame.K_s: Position(0, 1),
            pygame.K_d: Position(1, 0),
            pygame.K_w: Position(0, -1),
        }
        event = self._event_client.event()
        game_event = GameEvent(
            id=PlayerControlIds.MOVE_EVENT,
            payload=PlayerMoveEvent(
                object_id=GameObjectId("player"),
                direction=mapping[event.payload.key],
            ),
        )
        if event.payload.type == pygame.KEYDOWN:
            self._toggles.on(game_event)
        elif event.payload.type == pygame.KEYUP:
            self._toggles.off(game_event)


app = SeagullsApp()

component_factory = app.component_factory()
session_components = app.session_components()
scene_components = app.scene_components()


app.run(
    (PlayerControlIds.COMPONENT, lambda: PlayerControlsComponent(
        objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
        event_provider=lambda: scene_components.get(SessionComponents.EVENT_CLIENT).event().payload,
    )),
    (SessionComponents.PLUGIN_EVENT_CALLBACKS, lambda: tuple([
        (SceneEvents.open_scene(GameSceneId("index")), lambda: OpenScene(
            prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
            event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
            player_controls=scene_components.get(PlayerControlIds.COMPONENT),
            toggles=scene_components.get(SessionComponents.INPUT_TOGGLES_CLIENT),
        )()),
    ])),
    (GameComponentId[Tuple[SpriteSource, ...]]("sprite-sources"), lambda: tuple([
        SpriteSource(
            sprite_id=SpriteId("player"),
            image_name="kenney.tiny-dungeon/tilemap-packed",
            coordinates=Position(x=16, y=16*7),
            size=Size(16, 16),
        ),
    ])),
)
