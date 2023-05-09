from seagulls.cat_demos.app.environment._world_elements import (
    WorldElement,
    WorldElementClient, WorldElementId
)
from seagulls.cat_demos.app.gui._gui_client import ButtonConfig, GuiClient
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.debugging._debug_hud_client import DebugHud, DebugHudClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    SpriteId
)


class IndexScene(IExecutable):
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher
    _world_elements: WorldElementClient
    _debug_hud: DebugHudClient
    _gui_client: GuiClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
        world_elements: WorldElementClient,
        debug_hud: DebugHudClient,
        gui_client: GuiClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client
        self._world_elements = world_elements
        self._debug_hud = debug_hud
        self._gui_client = gui_client

    def __call__(self) -> None:
        self._spawn_environment()
        self._gui_client.create_mouse()
        self._gui_client.create_button(ButtonConfig(
            object_id=GameObjectId("menu:pew"),
            position=Position(600, 10),
            size=Size(height=49, width=190),
            sprite_id=SpriteId("menu-button"),
            hover_sprite_id=SpriteId("menu-button"),
            text="Pew Pew!",
        ))
        self._debug_hud.execute(DebugHud(show_fps=True))

    def _spawn_environment(self):
        for x in range(15):
            for y in range(15):
                self._world_elements.spawn(WorldElement(
                    object_id=GameObjectId(f"barrel::{x}.{y}"),
                    sprite_id=WorldElementId.BARREL,
                    position=Position(x=50 + (x * 32), y=50 + (y * 32)),
                ))
